#coding: utf-8

import json
from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import numpy as np

app = Flask(__name__)

def treinarIA():
    df = pd.read_csv('./datasets/noticias.csv')
    x_train, y_train = df['texto'], df['fake']
    with open('./datasets/stopwords.txt') as file:
        stopwords = file.read()

    # transformando os textos
    vectorizer = TfidfVectorizer(stop_words=stopwords.split() ,max_df=0.7)
    train_tfidf = vectorizer.fit_transform(x_train)

    # Criando o modelo classificador
    clf = XGBClassifier() 
    clf.fit(train_tfidf, y_train)
    
    return vectorizer, clf
    
vectorizer, clf = treinarIA()

def validaTweet(tweetContent):
    x_test = pd.DataFrame([[tweetContent]], columns=['texto'])
    test_tfidf = vectorizer.transform(x_test['texto'])
    pred = clf.predict(test_tfidf)
    return pred[0]

@app.route('/tweet', methods=['PUT'])
def verificatweet():
    resp = request.form['tt']
    mensagem = 'O BNDES possui seu próprio portal da transparencia onde você pode conferir a veracidade dessas informações. Acesse o portal: https://bit.ly/2Dztj8I'
    if validaTweet(resp)==1:
        f = open('./datasets/keywords.json', encoding='utf-8')
        keywords = json.loads(f.read())
        for i in keywords:
            if i  in resp.lower():
                mensagem = keywords[i]
                break
        return json.dumps({'fake':True, 'mensagem': mensagem})
    else:
        return json.dumps({'fake':False, 'mensagem': ''})


if __name__ == '__main__':
    app.run(debug=True)