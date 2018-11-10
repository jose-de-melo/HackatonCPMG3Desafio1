#coding: utf-8

from TwitterAPI import TwitterAPI
from datetime import datetime
import json, re

class Tweety:
    url_tweet = "https://twitter.com/{}/status/{}"

    keys = {
        "consumer_key":"09Zmx27gyLRh50GsPxa8S2LtQ",
        "consumer_secret":"uO7M4aGHGCK9oqxygrcgbxByCXcCLJMSTK72RmKBN9iLOXP4D3",
        "token_key":"1054111933014663168-VNtkKKAwLfNbpCpGZ5qsvczSMvRGZS",
        "token_secret":"6bfhp4oKxJ3lyVpKXyxu0jd2WGM66rSUXuWTmpzSsQZsv"
    }

    api = TwitterAPI(keys['consumer_key'],keys['consumer_secret'],
                     keys['token_key'],keys['token_secret'])

    '''end_points'''
    endp = {"search":"search/tweets", "post": "statuses/update"}

    '''Realiza uma busca pelo termo e retorna um TwitterResponse'''
    def search_term(self,term):
        return self.api.request(self.endp['search'], {'q':term, 'lang':'pt', 'count':10})

    def comment_tweet(self, screen_name, conteudo, id_tweet_conteudo):
        print(id_tweet_conteudo)
        return self.api.request(self.endp['post'], {'status': '@{}  '.format(screen_name) + conteudo, 'in_reply_to_status_id': id_tweet_conteudo})

    def retweet(self, screen_name, id_tweet , conteudo):
        return self.api.request(self.endp['post'], {'status': conteudo + '\n\n\n' + self.url_tweet.format(screen_name, id_tweet)})

    def teste_stream(self):
        r = self.api.request('statuses/filter', {'track': "AKADAK"})

        for item in r:
            print(item['text'] if 'text' in item else item)


    def filter(self,tw_response):
        jso = []
        for tw in tw_response:
            if(not tw['truncated']):
                twt = {}
                twt['id_tweet'] = tw['id']
                twt['username'] = tw['user']['name']
                twt['nickname'] = tw['user']['screen_name']
                twt['url_foto_perfil'] = tw['user']['profile_image_url']
                twt['data'] = self.parse_date(tw['created_at'])
                twt['conteudo'] = tw['text']
                jso.append(twt)

        return {"twetts":jso}

    def parse_date(self, date):
        pattern_in = "%a %b %d %H:%M:%S %z %Y"
        pattern_out = "%d/%m/%Y"
        time = datetime.strptime(date, pattern_in)
        return time.strftime(pattern_out)