from arbiter_helper import ArbiterHelper
import scrapping
import data_collecting


def prepare_work_list():
    return [10, 10], [data_collecting.work_gen(), scrapping.work_gen()],\
           [data_collecting.actor_init_task, scrapping.actor_init_task],\
           [data_collecting.actor_last_task, scrapping.actor_last_task]
    # liczebności aktorów do poszczególnych tasków
    # generatory funkcji do poszczególnych tasków
    # funkcje inicjalizujące dla aktorów poszczególnych tasków
    # funkcje kończące dla aktorów poszczególnych tasków


if __name__ == '__main__':
    actors_numbers, actors_gen_works, actors_init_works, actors_last_works = prepare_work_list()
    ArbiterHelper(actors_numbers, actors_gen_works, actors_init_works, actors_last_works)