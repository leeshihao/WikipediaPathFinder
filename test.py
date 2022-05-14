from pickletools import long1
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
import requests
import string
import pandas as pd

def tf_idf_summary(article):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={}&redirects='.format(article)
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e,'\nThe url connected with the error:' ,url)

    content = ''
    raw_corpus = []

    try:
        res_json = res.json()
        key = list(res_json['query']['pages'].keys())[0]
        content = (res_json['query']['pages'][key]['extract'])
    except:
        print('Error with JSON parsing, url request is bad')

    punctuation = [punct for punct in string.punctuation if punct != '.'] + ['\n']




    # remove stop words, punct, newlines
    for punct in punctuation:
        content = content.replace(punct, '')
    raw_corpus = nltk.sent_tokenize(content)

    long_sentence_corpus = list(filter(lambda sent: len(sent) > 30, raw_corpus))

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(long_sentence_corpus)
    #print(X.shape)

    tf_idf_sum = X.toarray().sum(axis = 0)

    tf_idf_weighted_sum = list(zip(vectorizer.get_feature_names_out(), tf_idf_sum))

    most_relevant_five = sorted(tf_idf_weighted_sum, key = lambda x: x[1],reverse = True)[0:10]
    return(most_relevant_five)

    #df = pd.DataFrame(data = X.toarray(),columns = vectorizer.get_feature_names_out())

    #print(df.iloc[:].sum(axis = 0))
    #print(tf_idf_sum)

