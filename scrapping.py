import asyncio
from functools import partial
from pulsar.api import command, get_actor, send


async def work(arg):
    print("ROBIĘ SCRAPPING...")
    '''
        TUTAJ UMIEŚĆ FUNKCJĘ
    '''
    await asyncio.sleep(1)


def work_gen():
    # można tutaj w pętli na przykład robić funckje z różnymi argumentami dla innych aktorów
    for i in range(5):
        yield partial(work, i)


def actor_init_task():
    print("INICJALIZUJĘ AKTORA")
    # to co chcemy żeby aktor robił podczas inicjalizacji


async def actor_last_task():
    print("KONIEC PRACY AKTORA")
    # to co chcemy żeby aktor robił podczas kończenia pracy, np. przesyłanie wyników

