class Recommender:
    def __init__(self, ads_database, recommender_engine):
        self._ads_database = ads_database
        self._recommender_engine = recommender_engine

    def add_ads(self, ads_data):
        """Add ads' data to the recommender database. The recommender will find
        the most similar ads amongst those, added with this method.

        Arguments:
        ads_data -- a list of AdData objects to be added to the database
        """
        self._ads_database.add_ads(ads_data)

    def archive_ads(self, ad_hyperlinks):
        """Adds ads', associated with given hyperlinks to the recommender's
        archive. The user will still be able to find ads similar to them, but
        they will not appear in find_similar results.

        Assumption:
        the hyperlink is unique for every advertisement
        and never changes

        Arguments:
        ad_hyperlinks -- a list of hyperlinks, to the offers to be archived

        """
        self._ads_database.archive_ads(ad_hyperlinks)

    def find_similar(self, ad_hyperlinks, ads_number):
        """Finds the most similar ads to a given one.

        Arguments:
        ad_hyperlinks -- a list of hyperlinks, to the ads,
                         for which similar ones are to be found.
                         ad_hyperlinks must exist in the recommender's database
                        - they must have been added in the past
        ads_number -- the maximal number of found similar ads

        """
        return self._recommender_engine.find_similar(ad_hyperlink, ads_number)
