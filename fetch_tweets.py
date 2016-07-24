#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
fetch_tweets.py
~~~~~~~~~~~~~~~

This script gets new tweets from the Twitter API, and adds them to
the rowling.json file.
"""

import collections
import json
import os
import shutil

from dateutil.parser import parse
import keyring
import tweepy


USERNAME = 'jk_rowling'


def setup_api():
    """
    Authorise the use of the Twitter API.  Returns a tweepy API object.
    """
    a = {
        attr: keyring.get_password("twitter", attr) for attr in
        ['consumerKey','consumerSecret','token','tokenSecret']
    }
    auth = tweepy.OAuthHandler(a['consumerKey'], a['consumerSecret'])
    auth.set_access_token(a['token'], a['tokenSecret'])
    return tweepy.API(auth)


def get_existing_tweets():
    if os.path.exists('%s.json' % USERNAME):
        data = json.loads(open('%s.json' % USERNAME).read())
        return collections.OrderedDict(
            sorted([(k, v) for (k, v) in data.items()],
            key=lambda t: t[1]['date'],
            reverse=True)
        )
    else:
        return {}


def write_tweets(tweets):
    pth = '%s.json' % USERNAME
    if os.path.exists(pth):
        shutil.move(pth, pth + '.bak')
    to_write = collections.OrderedDict(
        sorted([(k, v) for (k, v) in tweets.items()],
        key=lambda t: t[1]['date'],
        reverse=True)
    )
    json_str = json.dumps(to_write, indent=2)
    with open(pth, 'w') as outfile:
        outfile.write(json_str)


def get_tweets():
    tweets = get_existing_tweets()

    # Authorize Twitter, initialise Tweepy
    api = setup_api()

    # Make an initial request for the most recent tweets (200 is the max
    # allowed in a single request)
    new_tweets = api.user_timeline(screen_name=USERNAME, count=200)

    # Keep going until there are no more tweets left to get, or we
    # find tweets we've already saved.
    while len(new_tweets) > 0:

        print("Looking at tweets from %d..." % max(t.id for t in new_tweets))

        # We've gone far back enough that we already know all these tweets.
        # if all(t.id in tweets for t in new_tweets):
        #     break

        for t in new_tweets:
            t_data = t._json

            # Get the interesting data out
            id_str = t_data['id_str']
            text = t_data['text']
            date = parse(t_data['created_at'])

            # Have we seen this tweet before?  If so, skip it.
            if id_str in tweets:
                continue

            old_len = len(tweets)
            tweets[id_str] = {
                'url': 'http://twitter.com/%s/%s' % (USERNAME, id_str),
                'text': text,
                'date': str(date),
            }
            assert len(tweets) == old_len + 1

        new_tweets = api.user_timeline(screen_name=USERNAME,
                                       count=200,
                                       max_id=min(t.id for t in new_tweets)-1)

    write_tweets(tweets)


if __name__ == '__main__':
    get_tweets()