import random
from nltk.tokenize import RegexpTokenizer
import morfeusz


class RecommenderEngine:
    def __init__(self, ads_database):
        self._ads_database = ads_database
        self._stopwords = self._load_stopwords()

    def find_similar(self, ad_hyperlink, ads_number):
        result = []
        for _ in range(0, ads_number):
            result.append(random.randint(1, 5))
        return result

    def _prepare_vector_space_model(self):
        ads = self._ads_database.get_ads()
        ads_data = list(ads['description'])
        ads_data = self._string_tokenize(ads_data)
        ads_data = self._to_lowercase(ads_data)
        ads_data = self._remove_stopwords(ads_data)
        ads_data = self._lemmatize(ads_data)

    def _load_stopwords(self):
        stopwords = []
        with open('stopwords-pl', 'r') as stopwords_file:
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

    def _find_similar_ads(self, model, user_ad_indexes, number):
        pass
