import asyncio
from functools import partial
from pulsar.api import arbiter, command, spawn, send, ensure_future, Config
from pulsar.async.actor import get_actor


async def _default_work(arg):
    print(get_actor().name + ': Pracuję ' + str(arg))
    await asyncio.sleep(1)


def _default_works_gen():
    for i in range(100):
        yield partial(_default_work, i)


def _arbiter_init_task():
    print(str(get_actor().name) + ': Inicjalizuję arbitra')


async def _arbiter_last_task():
    print('arbiter: Wykonuję ostatnie zadanie')
    await asyncio.sleep(5)
    print('arbiter: Kończę pracę!')


def _default_actor_init_task():
    '''Pierwsze zadanie aktora'''
    print(str(get_actor().name) + ': Inicjalizuję aktora')


async def _default_actor_last_task():
    '''Ostatnie zadanie aktora'''
    print(str(get_actor().name) + ': Wykonuję ostatnie zadanie')
    await asyncio.sleep(1)
    print(str(get_actor().name) + ': Kończę pracę')


@command()
def _assign_work(request, number):
    actor = get_actor()
    work_list = actor.extra['work_gen_list'][number]
    try:
        task = next(work_list)
        print(actor.name + ': Przypisuję zadanie aktorowi ' + request.caller.name + ' numer ' + str(number))
        return task
    except StopIteration:
        pass


@command()
async def _stop_run_actor(request):
    get_actor().extra["running"] = False


class ArbiterHelper:
    def __init__(self, actors_counts,
                 work_list=[],
                 actors_init_tasks=[],
                 actors_last_tasks=[]):

        self._actors_counts = actors_counts
        if not work_list:
            self._work_list = []
            for i in range(0, len(actors_counts)):
                self._work_list.append(_default_works_gen())
        else:
            self._work_list = work_list
        self._arbiter_init_task = _arbiter_init_task
        self._arbiter_last_task = _arbiter_last_task
        self._actors_init_tasks = actors_init_tasks
        self._actors_last_tasks = actors_last_tasks
        self._initialize_arbiter()

    def __call__(self):
        ensure_future(self._arbiter_work())

    def _initialize_arbiter(self):
        arbiter(cfg=Config(workers=4, timeout=120))
        arbiter().extra['work_gen_list'] = self._work_list
        self._arbiter_init_task()
        arbiter()._loop.call_later(1, self)
        arbiter().start()

    async def _arbiter_work(self):
        self.actors = []
        arbiter().extra["data_actors"] = []

        if not self._actors_init_tasks:
            self._actors_init_tasks = [_default_actor_init_task] * len(self._actors_counts)

        if not self._actors_last_tasks:
            self._actors_last_tasks = [_default_actor_last_task] * len(self._actors_counts)

        for i in range(len(self._actors_counts)):
            for j in range(self._actors_counts[i]):
                actor_name = 'actor({}, {})'.format(i, j)
                print(get_actor().name + ': Tworzę aktora ' + actor_name + '...')

                actor = await spawn(name=actor_name, start=partial(ArbiterHelper._init_actor, number=i, sec_number=j,
                                                                   init_func=partial(self._actors_init_tasks[i]),
                                                                   last_job=partial(self._actors_last_tasks[i])))
                self.actors.append(actor)
                if i == 0:
                    arbiter().extra["data_actors"].append(actor)

        while True in [actor.is_alive() for actor in
                       self.actors[self._actors_counts[0]:-self._actors_counts[2]]]:
            await asyncio.sleep(1)

        await asyncio.sleep(5)

        for actor in self.actors[:self._actors_counts[0]]:
            await send(actor, '_stop_run_actor')

        await send(self.actors[-1], '_stop_run_actor')

        await asyncio.sleep(5)
        await self._arbiter_last_task()

        try:
            arbiter().stop()
        except PermissionError:  # Windows
            quit()

    @staticmethod
    def _init_actor(_, number, sec_number, init_func, last_job):
        get_actor().extra['number'] = number
        get_actor().extra['sec_number'] = sec_number
        init_func()
        ensure_future(ArbiterHelper._actor_loop(last_job))

    @staticmethod
    async def _actor_loop(last_job):
        actor = get_actor()
        print(actor.name + ': Startuję!')
        while True:
            order = await send(get_actor().monitor, '_assign_work', get_actor().extra['number'])
            if order is None:
                await last_job()
                get_actor().stop()
                await asyncio.sleep(2)
            else:
                await order()


if __name__ == '__main__':
    x = ArbiterHelper([5, 5])
