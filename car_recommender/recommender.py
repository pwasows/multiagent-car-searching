from ad_data import AdData
from nltk.tokenize import RegexpTokenizer
import morfeusz
from gensim import corpora, models, similarities
import pandas as pd


class Recommender:
    def __init__(self, ads_file):
        #TODO: load ads_file
        self._stopwords = self._load_stopwords()
        self._lsi_model = models.LsiModel.load('car_recommender/allegro_model_lsi')
        self._tf_idf_model = models.TfidfModel.load('car_recommender/allegro_tf_idf_model')
        self._dictionary = corpora.Dictionary.load('car_recommender/allegro_dictionary')
        self._model_index = \
            similarities.Similarity(output_prefix='sim_matrix_tmp',
                                    corpus=None,
                                    num_features=self._lsi_model.num_topics)
        self._storage = pd.DataFrame(columns=['hyperlink', 'description'])
        self._storage = self._storage.set_index('hyperlink')

    def add_ads(self, ads_data):
        """Add ads' data to the recommender database. The recommender will find
        the most similar ads amongst those, added with this method.

        Arguments:
        ads_data -- a list of AdData objects to be added to the database
        """

        if type(ads_data) is AdData:
            ads_data = [ads_data]
        elif type(ads_data) is not list:
            raise TypeError

        descriptions = []
        for ad in ads_data:
            self._storage.loc[ad.hyperlink] = [ad.description]
            descriptions.append(ad.description)

        self._add_to_similarity_matrix(descriptions)

    def get_ad_links(self):
        '''Returns a list of links to all ads, present in the database'''
        return self._storage.index.values.tolist()

    def find_similar(self, ad_hyperlinks, ads_number):
        """Finds the most similar ads to a given one.

        Arguments:
        ad_hyperlinks -- a list of hyperlinks, to the ads,
                         for which similar ones are to be found.
                         ad_hyperlinks must exist in the recommender's database
                        - they must have been added in the past
        ads_number -- the maximal number of found similar ads
        """
        results = []
        for link in ad_hyperlinks:
            try:
                ad_row = self._storage.index.get_loc(link)
            except KeyError:
                print('Ad not found: ' + link)
            similarities = self._model_index.similarity_by_id(ad_row)
            results.append(similarities)

        result = sum(results)
        # negation to sort in descending order
        best_fit = (-result).argsort()[:ads_number]


        best_fit_links = []
        for i in best_fit:
            best_fit_links.append(self._storage.iloc[i])
        return best_fit_links

    def _add_to_similarity_matrix(self, descriptions):
        description_lsi = self._texts_to_lsi(descriptions)
        self._model_index.add_documents(description_lsi)

    def _texts_to_lsi(self, descriptions):
        transformed = self._tokenize(descriptions)
        transformed = self._to_lowercase(transformed)
        transformed = self._remove_stopwords(transformed)
        transformed = self._lemmatize(transformed)
        corpus = self._prepare_tf_idf_corpus(transformed)
        return self._lsi_model[corpus]

    def _prepare_tf_idf_corpus(self, texts):
        tf_idf_corpus = [self._dictionary.doc2bow(text) for text in texts]
        return self._tf_idf_model[tf_idf_corpus]

    def _load_stopwords(self):
        stopwords = []
        with open('car_recommender/stopwords-pl', 'r') as stopwords_file:
            stopwords = stopwords_file.readlines()
        stopwords = [word.strip() for word in stopwords]
        return set(stopwords)

    def _tokenize(self, texts):
        '''Turns documents into alphabetic-only tokens'''
        tokenizer = RegexpTokenizer(r'[a-zA-ZĄąĆćĘęŁłŃńÓóŚśŻżŹź]+')

        result = []
        for text in texts:
            result.append(tokenizer.tokenize(text))

        return result

    def _to_lowercase(self, texts):
        result = []
        for text in texts:
            result.append([word.lower() for word in text])

        return result

    def _remove_stopwords(self, texts):
        result = []
        for text in texts:
            result.append([word for word in text
                           if word not in self._stopwords])

        return result

    def _lemmatize(self, texts):
        result = []
        for text in texts:
            text_lemmas = []

            for word in text:
                lemma = morfeusz.analyse(word, expand_tags=False)[0][0][1]
                # morfeusz returns None if has no clue, what the word he got
                if lemma:
                    text_lemmas.append(lemma)

            result.append(text_lemmas)

        return result
