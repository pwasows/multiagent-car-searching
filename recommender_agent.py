import asyncio
from functools import partial
from pulsar.api import command, get_actor, send
import sys
sys.path.append('car_recommender')
from recommender import Recommender
import json


# SCRAPER_AGENT
# zakładam, że tak się nazywa agent, który będzie dodawał nowe oferty do bazy

# UI_AGENT
# zakładam, że tak się nazywa agent, który będzie wysyłał żądania od uzytkownika:
#   - prosbe o przeslanie linkow do ofert, ktore sa w bazie tego rekomendatora
#   - prosbe o zaproponowanie ofert podobnych, do przeslanych


async def recommender_job(ads_file):
    get_actor().extra["running"] = True
    actor_number = get_actor().extra['sec_number']
    print("Recommender starts. Data file: " + ads_file)

    # tworzę obiekt implementujący rekomendację samochodów,
    # przyjmujący nowe ogłoszenia i zawierający bazę ściągniętych ogłoszeń
    recommender = Recommender(ads_file)

    while True:
        await asyncio.sleep(1)

        # sprawdzam, czy przyszły nowe wiadomości od innych agentów
        scraper_data = await send(get_actor().monitor, '_recommender_get_data', actor_number, 'scrapper_data')
        # zakładam, że jeśli nie ma nowych wiadomości od scrapera,
        # to get_data zwróci None
        if scraper_data is not None:
            recommender.add_ads(scraper_data)

        ui_message = await send(get_actor().monitor, '_recommender_get_data', get_actor().extra['sec_number'],
                                'user_input_data')
        if ui_message is not None:
            # problem(?): jeśli różni agenci-rekomendatorzy
            # będą przechowywali różne oferty, to trzeba żądanie o zwrócenie
            # ofert podobnych do wskazanych skierować do tego agenta, który
            # zawiera te oferty
            # albo agenci-rekomendatorzy muszą przesłać pomiędzy sobą
            # reprezentacje wektorowe wskazanych ogłoszeń, żeby znaleźć
            # u siebie podobne do nich oferty
            response = recommender.find_similar(ui_message, 5)
            await send(get_actor().monitor, '_recommender_store_data', actor_number, 'user_output_data', response)
            break

        '''
        Jeśli zdecydujemy się na wariant, w którym rekomendatorzy wymieniają
        pomiędzy sobą informacje, to tutaj można dodać obsługę wiadomości
        pomiędzy nimi

        '''

    print('Goodbye!')


def work_gen():
    # ads_files to różne pliki z ofertami, które ładujemy do baz rekomendatorów
    ads_files = ['ads0', 'ads1', 'ads2', 'ads3', 'ads4', 'ads5', 'ads6', 'ads7', 'ads8', 'ads9']
    for i in ads_files:
        yield partial(recommender_job, i)


# To nie wiem, czy potrzebne, jakieś zadania wstępne można tu wykonać
def actor_init_task():
    print("INICJALIZUJĘ REKOMENDATORA")
    # to co chcemy żeby aktor robił podczas inicjalizacji


async def actor_last_task():
    print("KONIEC PRACY REKOMENDATORA")


# Poniższe funkcje są związane z systemem komunikacji pomiędzy data collector actorami,
# a aktorami implementowanymi w tych plikach

# Prosimy arbitra, aby przekazał dane tam gdzie trzeba
@command()
async def _recommender_store_data(_, number, data_name, data):
    await send(get_actor().extra['data_actors'][number], '_recommender_store_data_command', data_name, data)


@command()
async def _recommender_get_data(_, number, data_name):
    return await send(get_actor().extra['data_actors'][number], '_recommender_get_data_command', data_name)


# poniższe komendy są wykonywane po stronie data collectora
@command()
def _recommender_store_data_command(_, data_name, data):
    get_actor().extra[data_name].append(data)


@command()
def _recommender_get_data_command(_, data_name):
    data = get_actor().extra[data_name]
    if data:
        return data
    return None
