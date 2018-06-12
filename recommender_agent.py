import asyncio
from functools import partial
from pulsar.api import command, get_actor, send
from car_recommender.recommender import Recommender

import json

# zakładam, że tak się nazywa agent, który będzie dodawał nowe oferty do bazy
SCRAPER_AGENT = 10

# zakładam, że tak się nazywa agent, który będzie wysyłał żądania od uzytkownika:
#   - prosbe o przeslanie linkow do ofert, ktore sa w bazie tego rekomendatora
#   - prosbe o zaproponowanie ofert podobnych, do przeslanych
UI_AGENT = 15

async def recommender_job(ads_file):
    print("Recommender starts. Data file: " + ads_file)

    # tworzę obiekt implementujący rekomendację samochodów,
    # przyjmujący nowe ogłoszenia i zawierający bazę ściągniętych ogłoszeń
    recommender = Recommender(ads_file)

    while True:
        await asyncio.sleep(1)

        # sprawdzam, czy przyszły nowe wiadomości od innych agentów
        # zakładam, że wysyłają oni jsony w takiej postaci:
        # {'message': 'treść wiadomości', 'data': <ewentualne dane>}
        # {''}
        scraper_message = get_data(SCRAPER_AGENT)
        # zakładam, że jeśli nie ma nowych wiadomości od scrapera,
        # to get_data zwróci None
        if scraper_message is not None:
            scraper_message = json.loads(scraper_message)
            if scraper_message['message'] == 'ADD_ADS':
                #spodziewam się w scraper_message['data'] listy obiektow AdData
                recommender.add_ads(scraper_message['data'])
            else:
                print('Invalid message from ' + str(SCRAPER_AGENT) +
                      str(scraper_message))

        ui_message = get_data(UI_AGENT)
        if ui_message is not None:
            ui_message = json.loads(ui_message) 
            # problem(?): jeśli różni agenci-rekomendatorzy
            # będą przechowywali różne oferty, to trzeba żądanie o zwrócenie
            # ofert podobnych do wskazanych skierować do tego agenta, który
            # zawiera te oferty
            # albo agenci-rekomendatorzy muszą przesłać pomiędzy sobą
            # reprezentacje wektorowe wskazanych ogłoszeń, żeby znaleźć
            # u siebie podobne do nich oferty
            if ui_message['message'] == 'GET_ADS_LINKS':
                response = {'message': 'GET_ADS_LINKS_RESPONSE',
                            'data': recommender.get_ad_links()}
                store_data(UI_AGENT, json.dumps(response),
                           'GET_ADS_LINKS_RESPONSE')
            elif ui_message['message'] == 'FIND_SIMILAR':
                response = {'message': 'FIND_SIMILAR_RESPONSE',
                            'data':
                            recommender.find_similar(ui_message['data'], 5)
                            }
                store_data(UI_AGENT, json.dumps(response),
                           'FIND_SIMILAR_RESPONSE')

        '''
        Jeśli zdecydujemy się na wariant, w którym rekomendatorzy wymieniają
        pomiędzy sobą informacje, to tutaj można dodać obsługę wiadomości
        pomiędzy nimi

        '''

    print('Goodbye!')


def work_gen():
    # ads_files to różne pliki z ofertami, które ładujemy do baz rekomendatorów
    ads_files = ['ads1', 'ads2']
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
async def store_data(_, number, data):
    await send(get_actor().extra['data_actors'][number], 'store_data_command', data)


@command()
async def get_data(_, number):
    return await send(get_actor().extra['data_actors'][number], 'get_data_command')


# poniższe komendy są wykonywane po stronie data collectora
@command()
def store_data_command(_, data):
    get_actor().extra['some_data'].append(data)


@command()
def get_data_command(request):
    return get_actor().extra['some_data']