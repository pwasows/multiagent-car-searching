import random
from nltk.tokenize import RegexpTokenizer
import morfeusz
from gensim import corpora, models, similarities, matutils


class RecommenderEngine:
    def __init__(self, ads_database):
        self._ads_database = ads_database
        self._stopwords = self._load_stopwords()

    def find_similar(self, ad_hyperlink, ads_number):
        model, corpus = self._prepare_vector_space_model()
        similarity_matrix = self._prepare_similarity_matrix(LSI_model,
                                                            tf_idf_corpus)
        ad_row = self._ads_database.index.get_loc(ad_hyperlink)

        #TODO: get ads_number most similar ads

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
        dictionary = self._prepare_dictionary(ads_data)
        corpus = self._prepare_corpus(ads_data, dictionary)
        tf_idf_model = self._prepare_tf_idf_model(corpus)
        tf_idf_corpus = self._prepare_tf_idf_corpus(corpus, tf_idf_model)
        LSI_model = self._prepare_LSI_model(tf_idf_corpus, dictionary)
        return LSI_model, tf_idf_model


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

    def _prepare_dictionary(self, texts):
        return corpora.Dictionary(texts)

    def _prepare_corpus(self, texts, dictionary):
        return [dictionary.doc2bow(text) for text in texts]

    def _prepare_tf_idf_model(self, corpus):
        return models.TfidfModel(corpus)

    def _prepare_tf_idf_corpus(self, corpus, tf_idf_model):
        return tf_idf_model[corpus]

    def _prepare_LSI_model(self, corpus, dictionary):
        return models.LsiModel(corpus, id2word=dictionary, num_topics=30)

    def _prepare_similarity_matrix(self, model, corpus):
        return similarities.MatrixSimilarity(model[corpus])

    def _find_similar_ads(self, model, user_ad_indexes, number):
        pass
