import asyncio
from functools import partial
from pulsar.api import command, get_actor, send


async def work():
    get_actor().extra["running"] = True
    get_actor().extra["scrapper_data"] = []
    last_scrapper_data_size = 0

    while get_actor().extra["running"]:
        scrapper_data_len = len(get_actor().extra["scrapper_data"])
        if last_scrapper_data_size != scrapper_data_len:
            print('{} Wyswietlam nowe dane:'.format(get_actor().name))
            for i in range(last_scrapper_data_size, scrapper_data_len):
                print(get_actor().extra["scrapper_data"][i])
            last_scrapper_data_size = scrapper_data_len
        await asyncio.sleep(1)


def work_gen():
    for i in range(10):
        yield partial(work)


def actor_init_task():
    print("INICJALIZUJĘ DATA KOLEKTORA")
    # to co chcemy żeby aktor robił podczas inicjalizacji


async def actor_last_task():
    print("KONIEC PRACY DATA KOLEKTORA")
    # to co chcemy żeby aktor robił podczas kończenia pracy, np. przesyłanie wyników