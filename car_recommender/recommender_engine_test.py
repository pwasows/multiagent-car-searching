from recommender_engine import RecommenderEngine


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

data = engine._lemmatize(data)
#print(data) # OK
