from recommender_engine import RecommenderEngine
from gensim import corpora
from time import time


test_data = ''
with open('test_pl_data', 'r') as test_data_file:
    #7 lines
    test_data = [line.strip() for line in test_data_file.readlines()]


engine = RecommenderEngine([])
#print(engine._stopwords) # OK

data = engine._tokenize(test_data)
#print(data) # OK

data = engine._to_lowercase(data)
#print(data) # OK

data = engine._remove_stopwords(data)
#print(data) # OK

start = time()
data = engine._lemmatize(data)
print('lemmatization time: ' + str(time() - start))
#print(data) # OK

dictionary = engine._prepare_dictionary(data)
# print(dictionary)

corpus = engine._prepare_corpus(data, dictionary)
# print(corpus[0])

tfidf_model = engine._prepare_tf_idf_model(corpus)
#print(tfidf_model)

tf_idf_corpus = engine._prepare_tf_idf_corpus(corpus, tfidf_model)
# print(tf_idf_corpus[0])

print(dir(dictionary))
print(len(dictionary))

LSI_model = engine._prepare_LSI_model(tf_idf_corpus, dictionary)
print(dir(LSI_model))

sim_mx = engine._prepare_similarity_matrix(LSI_model,
                                           tf_idf_corpus,
                                           data)

engine.find_similar()