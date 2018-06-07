from ad_data import AdData
from ads_database import AdsDatabase

if __name__ == '__main__':
    ads_database = AdsDatabase()

    ads_database.add_ads(AdData(description='abc', tags=[('aa', 'bb')],
                        hyperlink='https://google.com'))
    ads_database.add_ads(AdData(description='def', tags=[('aa', 'cc')],
                        hyperlink='https://yahoo.com'))
    ads_database.archive_ads('https://yahoo.com')
    print(ads_database.get_active_ads())
