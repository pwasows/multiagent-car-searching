from recommender import Recommender
from ad_data import AdData
from ads_database import AdsDatabase
from recommender_engine import RecommenderEngine

if __name__ == '__main__':
    ads_database = AdsDatabase()
    recommender_engine = RecommenderEngine(ads_database)

    recommender = Recommender(ads_database, recommender_engine)
    recommender.add_ads(AdData(description='abc', tags=[('aa', 'bb')],
                        hyperlink='https://google.com'))
    recommender.add_ads(AdData(description='def', tags=[('aa', 'cc')],
                        hyperlink='https://yahoo.com'))
    recommender.archive_ads('https://yahoo.com')
    print(recommender.find_similar('https://google.com', 5))
