import asyncio
from functools import partial
from pulsar.api import command, get_actor, send
import sys
sys.path.append('car_recommender')
from recommender import Recommender, ADS_FILES

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

        ui_message = await send(get_actor().monitor, '_recommender_get_data', get_actor().extra['sec_number'],
                                'user_input_data')
        if ui_message is not None:
            for single_link in ui_message:
                ad_vector = recommender.get_ad_vector(single_link)
                if ad_vector is not None:
                    await send(get_actor().monitor, '_recommender_send_to_all', 'user_ad_vectors', ad_vector)

            await asyncio.sleep(5)

            user_ads = await send(get_actor().monitor, '_recommender_get_data', get_actor().extra['sec_number'],
                                  'user_ad_vectors')
            if user_ads is None:
                response = 'Nie znaleziono ad_vector usera w recommenderze {}'.format(get_actor().extra['sec_number'])
            else:
                response = recommender.find_similar_to_vec(user_ads, 1)
            await send(get_actor().monitor, '_recommender_store_data', actor_number, 'user_output_data', response)
            break


def work_gen():
    # ads_files to różne pliki z ofertami, które ładujemy do baz rekomendatorów
    for i in ADS_FILES[:-1]:
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
async def _recommender_send_to_all(_, data_name, data):
    for act in get_actor().extra['data_actors']:
        await send(act, '_recommender_store_data_command', data_name, data)


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
