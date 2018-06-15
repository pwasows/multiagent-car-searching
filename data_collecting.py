import asyncio
from functools import partial
from pulsar.api import command, get_actor, send


async def work():
    get_actor().extra["running"] = True
    get_actor().extra["user_input_data"] = []
    get_actor().extra["user_output_data"] = []
    get_actor().extra["user_ad_vectors"] = []


    while get_actor().extra["running"]:
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