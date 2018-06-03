import asyncio
from pulsar.api import command, get_actor, send

async def work(index, name, query):

    await asyncio.sleep(config.middle_task_wait)


def work_gen(query):
    query = get_actor().extra['dict'].doc2bow(query)
    query = get_actor().extra['tfidf'][query]
    query = get_actor().extra['lsi'][query]

    for name, index in gen:
        yield partial(work, index, name, query)


def arbiter_init_task():
    get_actor().extra['dict'] = corpora.Dictionary.load(config.dictionary_path)
    get_actor().extra['tfidf'] = models.TfidfModel.load(config.tfidf_model_path)
    get_actor().extra['lsi'] = models.LsiModel.load(config.lsi_model_path)
    get_actor().extra['results'] = []


async def arbiter_last_task():
    print(get_actor().name + ': Porządkuję wyniki')
    result = sorted(get_actor().extra['results'], key=lambda x: -x['score'])[:config.results_count]
    print('\n\n')
    for elem in result:
        print(elem)
    print('\n\n')
    with open(config.search_result_path, 'wb') as f:
        pickle.dump(result, f)
    print(get_actor().name + ': Wyniki zapisano do ' + config.search_result_path)


def actor_init_task():
    get_actor().extra['gh'] = GHInterface()
    get_actor().extra['result'] = []


async def actor_last_task():
    print(get_actor().name + ': Przesyłam wyniki')
    result = get_actor().extra['result']
    await send(get_actor().monitor, 'save_partial_result', result)


@command()
def save_partial_result(_, result):
    get_actor().extra['results'] += result

