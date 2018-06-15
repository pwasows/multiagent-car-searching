from arbiter_helper import ArbiterHelper
import data_collecting
import recommender_agent
import user_ui_agent


def prepare_work_list():
    return [10, 10, 1],\
           [data_collecting.work_gen(), recommender_agent.work_gen(), user_ui_agent.work_gen()],\
           [data_collecting.actor_init_task, recommender_agent.actor_init_task, user_ui_agent.actor_init_task],\
           [data_collecting.actor_last_task, recommender_agent.actor_last_task, user_ui_agent.actor_last_task]
    # liczebności aktorów do poszczególnych tasków
    # generatory funkcji do poszczególnych tasków
    # funkcje inicjalizujące dla aktorów poszczególnych tasków
    # funkcje kończące dla aktorów poszczególnych tasków


if __name__ == '__main__':
    actors_numbers, actors_gen_works, actors_init_works, actors_last_works = prepare_work_list()
    ArbiterHelper(actors_numbers, actors_gen_works, actors_init_works, actors_last_works)