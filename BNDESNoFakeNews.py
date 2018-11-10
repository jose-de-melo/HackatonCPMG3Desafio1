#coding: utf-8

import json
from ModuloTwitter import twitter_module as tm
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

'''
 Rota para renderizar a página inicial da aplicação
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", status=201)
'''
def responder_tweet(id, screen_name):
    tweety = tm.Tweety()
    tweety.comment_tweet(screen_name, 'CDV ? Tá maluco ? Eu em', id)


'''Busca por tweets que possuam determinado termo usando módulo'''
def search_tweets(termo):
    tweety = tm.Tweety()
    result = tweety.search_term(termo)
   # tweety.retweet('https://twitter.com/joseslv13/status/1058793300931547136', "Teste retweet")
    return tweety.filter(result)

'''End-point para recuperar informações sobre o heroi'''
@app.route('/tweets/<termo>', methods=['GET'])
def search(termo):
    twetts = search_tweets("'"+termo+"'")

###    for tt in twetts['twetts'] :
###        #print(tt['conteudo'])
###        resp = requests.put('http://100.64.15.168:5000/tweet', data={'tt': tt['conteudo']})
###        print(resp.text)

    #twetts['tweets'] = "Acabou!"

    #for t in twetts['twetts']:
    #    responder_tweet(t['id_tweet'], t['nickname'])

    return json.dumps(twetts)

'''__main__'''
if __name__ == "__main__":
    app.run(debug=True, port=8080)
