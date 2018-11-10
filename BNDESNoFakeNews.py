#coding: utf-8

import json
from ModuloTwitter import twitter_module as tm
import requests
from flask import Flask, render_template, request


fake_count = 0

app = Flask(__name__)

def responder_tweet(id, screen_name, mensagem):
    tweety = tm.Tweety()
    print("CHEGOU")
    tweety.comment_tweet(screen_name, mensagem, id)


'''Busca por tweets que possuam determinado termo usando módulo'''
def search_tweets(termo):
    tweety = tm.Tweety()
    result = tweety.search_term(termo)
    return tweety.filter(result)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', nFakes = fake_count)

'''End-point para recuperar informações sobre o heroi'''
@app.route('/tweets/<termo>', methods=['GET'])
def search(termo='BNDES'):
    global fake_count
    twetts = search_tweets("'"+termo+"'")

    
    for tt in twetts['twetts'] :
        resp = requests.put('http://127.0.0.1:5000/tweet', data={'tt': tt['conteudo']})

        respJson = json.loads(resp.text)

        print(respJson)
        if respJson['fake'] == True:
            print('FAKE')
            #responder_tweet(tt['id_tweet'], tt['nickname'], respJson['mensagem'])
            fake_count += 1
        else:
            print("THIS IS A REAL NEWS!")
            continue

    return json.dumps(twetts)

'''__main__'''
if __name__ == "__main__":
    app.run(debug=True, port=8080)
