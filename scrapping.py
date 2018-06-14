import asyncio
from functools import partial
from pulsar.api import command, get_actor, send


async def work2(arg):
    get_actor().extra["running"] = True
    print("ROBIĘ SCRAPPING 2...")
    '''
        TUTAJ UMIEŚĆ FUNKCJĘ 2
    '''

    # actor_number = get_actor().extra['sec_number']
    # await send(get_actor().monitor, 'scrapper_store_data', actor_number, 'dupa{}'.format(actor_number))
    while get_actor().extra["running"]:
        await asyncio.sleep(1)


async def work(arg):
    get_actor().extra["running"] = True
    print("ROBIĘ SCRAPPING...")
    '''
        TUTAJ UMIEŚĆ FUNKCJĘ
    '''

    # actor_number = get_actor().extra['sec_number']
    # await asyncio.sleep(5)
    # print(await send(get_actor().monitor, 'scrapper_get_data', actor_number + 1))
    while get_actor().extra["running"]:
        await asyncio.sleep(1)


def work_gen():
    for i in range(5):
        yield partial(work, i)
        yield partial(work2, i)


def actor_init_task():
    print("INICJALIZUJĘ SCRAPPERA")
    # to co chcemy żeby aktor robił podczas inicjalizacji


async def actor_last_task():
    print("KONIEC PRACY SCRAPPERA")
    # to co chcemy żeby aktor robił podczas kończenia pracy, np. przesyłanie wyników


# prosimy arbitra, aby przekazał dane tam gdzie trzeba
@command()
async def scrapper_store_data(_, number, data):
    await send(get_actor().extra['data_actors'][number], 'scrapper_store_data_command', data)


@command()
async def scrapper_get_data(_, number):
    return await send(get_actor().extra['data_actors'][number], 'scrapper_get_data_command')


# poniższe komendy są wykonywane po stronie data collectora
@command()
def scrapper_store_data_command(_, data):
    get_actor().extra['scrapper_data'].append(data)


@command()
def scrapper_get_data_command(request):
    return get_actor().extra['scrapper_data']
