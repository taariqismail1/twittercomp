#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 16:38:31 2021

@author: taariqismail
"""

from flask import Flask, jsonify, request, render_template
import random
import requests
from random import shuffle

app = Flask(__name__)



# Twitter API function

def get_winners(url, number):
    key = 'a0AEqCf5tsBT5d3XVOiZiGbHU'
    secret = 'RrV6ciA2WNJr3IZLOyPFrL1NbkMTYXQBkq4WMZo72pschemMAB'
    auth_url = 'https://api.twitter.com/oauth2/token'
    data = {'grant_type': 'client_credentials'}
    auth_resp = requests.post(auth_url, auth=(key, secret), data=data)
    token = auth_resp.json()['access_token']

    tweet_id = url.split('/')[-1].split('?')[0]
    url = 'https://api.twitter.com/1.1/statuses/retweets/%s.json?count=100' % tweet_id
    headers = {'Authorization': 'Bearer %s' % token}
    retweets_resp = requests.get(url, headers=headers)
    retweets = retweets_resp.json()
    
    retweeters = [r['user']['screen_name'] for r in retweets]
    
    all_retweeters = list(retweeters)
    shuffle(all_retweeters)
    winners = all_retweeters[:number]
    winners = ["@"+str(i)+"<br>" for i in winners]

    return(''.join(winners))
    




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        url = request.form['tweet']
        numberWinners = request.form['numberWinners']
        tweet_id = url.split('/')[-1].split('?')[0]
        if not tweet_id.isdigit():
                return render_template('index.html', message='Invalid tweet URL')
            
            
            
        return render_template('success.html', winners = get_winners(url, int(numberWinners)))








if __name__ == '__main__':
    app.debug = True
    app.run()