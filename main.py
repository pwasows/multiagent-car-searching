from arbiter_helper import ArbiterHelper


def prepare_work_list():
    return [10], [], []



if __name__ == '__main__':
    actors_number, actors_init_works, actors_last_works = prepare_work_list()
    ArbiterHelper(actors_number, actors_init_works, actors_last_works)