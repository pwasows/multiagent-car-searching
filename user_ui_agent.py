import asyncio
from functools import partial
from pulsar.api import command, get_actor, send
import socket
import time


async def work():
    get_actor().extra["running"] = True

    # Tworzymy TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Łączenie socketu do portu gdzie działa serwer
    server_address = ('localhost', 10000)
    print('Łączenie z aplikacją kliencką {0} port {1}\n'.format(*server_address))

    connected = False
    while not connected:
        try:
            sock.connect(server_address)
            connected = True
        except ConnectionRefusedError:
            pass

    try:
        urls = []

        while True:
            data = sock.recv(256)
            if not data:
                break
            data = data.decode()
            if data == 'END_OF_URLS':
                print("Koniec URLi\n")
                await send(get_actor().monitor, '_user_io_store_data', urls)
                break
            print('Agent otrzymał URL "{}"\n'.format(data))
            urls.append(data)

        while get_actor().extra["running"]:
            data = await send(get_actor().monitor, '_user_io_get_data')
            if data is not None:
                sock.sendall(data.encode())
            await asyncio.sleep(1)

        sock.sendall('END_OF_RESULTS'.encode())

    finally:
        print('Zamykanie socketu\n')
        time.sleep(1)
        sock.close()


def work_gen():
    yield partial(work)


def actor_init_task():
    print("INICJALIZUJĘ AGENTA UI")
    # to co chcemy żeby aktor robił podczas inicjalizacji


async def actor_last_task():
    print("KONIEC PRACY AGENTA UI")
    # to co chcemy żeby aktor robił podczas kończenia pracy, np. przesyłanie wyników


# prosimy arbitra, aby przekazał dane tam gdzie trzeba
@command()
async def _user_io_store_data(_, data):
    data_actors = get_actor().extra['data_actors']
    for act in data_actors:
        await send(act, '_user_io_store_data_command', data)


@command()
async def _user_io_get_data(_,):
    data_actors = get_actor().extra['data_actors']
    results = []
    for act in data_actors:
        data = await send(act, '_user_io_get_data_command')
        if data:
            results.extend(data)
    if results:
        return "\n".join(str(x) for x in results)
    else:
        return None


# poniższe komendy są wykonywane po stronie data collectora
@command()
def _user_io_store_data_command(_, data):
    get_actor().extra['user_input_data'] = data


@command()
def _user_io_get_data_command(request):
    result = get_actor().extra['user_output_data']
    get_actor().extra['user_output_data'] = []
    return result
