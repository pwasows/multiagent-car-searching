import random


class RecommenderEngine:
    def __init__(self, ads_database):
        pass

    def find_similar(self, ad_hyperlink, ads_number):
        result = []
        for _ in range(0, ads_number):
            result.append(random.randint(1, 5))
        return result
