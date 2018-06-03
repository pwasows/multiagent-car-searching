from arbiter_helper import ArbiterHelper
import scrapping


def prepare_work_list():
    return [10], [scrapping.work_gen()], [], []
    # liczebności aktorów do poszczególnych tasków
    # generatory funkcji do poszczególnych tasków
    # funkcje inicjalizujące dla aktorów poszczególnych tasków
    # funkcje kończące dla aktorów poszczególnych tasków


if __name__ == '__main__':
    actors_numbers, actors_gen_works, actors_init_works, actors_last_works = prepare_work_list()
    ArbiterHelper(actors_numbers, actors_gen_works, actors_init_works, actors_last_works)