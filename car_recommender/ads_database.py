from ad_data import AdData
import pandas as pd


class AdsDatabase:
    def __init__(self):
        storage = pd.DataFrame(columns=['hyperlink', 'description', 'tags',
                                        'active'])
        self._storage = storage.set_index('hyperlink')

    def add_ads(self, ads_data):
        if type(ads_data) is AdData:
            ads_data = [ads_data]
        elif type(ads_data) is not list:
            raise TypeError

        for ad in ads_data:
            self._storage.loc[ad.hyperlink] = [ad.description, ad.tags, True]

    def archive_ads(self, ad_hyperlinks):
        if type(ad_hyperlinks) is str:
            ad_hyperlinks = [ad_hyperlinks]
        elif type(ad_hyperlinks) is not list:
            raise TypeError

        for hyperlink in ad_hyperlinks:
            self._storage.loc[hyperlink]['active'] = False

    def get_ads(self):
        return self._storage

    def get_active_ads(self):
        active_ads = self._storage['active'] == True
        return self._storage.loc[active_ads]
