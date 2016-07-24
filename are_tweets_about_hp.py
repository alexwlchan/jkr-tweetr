#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
are_tweets_about_hp.py
~~~~~~~~~~~~~~~~~~~~~~

This is a helper app I wrote to help me sort out tweets that are about
Harry Potter, and those that aren't.
"""

from flask import Flask, render_template, request, redirect
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

from fetch_tweets import get_existing_tweets, write_tweets, USERNAME


app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'fizzing-whizzbee'

PTH = '%s.json' % USERNAME


@app.route('/')
def alltweets_page():
    print(request.args)
    tweets = get_existing_tweets()
    if request.args.get('filter') == 'unsorted':
        tweets = {t_id: t for t_id, t in tweets.items() if 'is_about_hp' not in t}
    count = len(tweets)
    excluded = len([t for t in tweets.values() if not t.get('is_about_hp', True)])
    not_posted = len([t for t in tweets.values() if t.get('is_about_hp', False) and not t.get('is_in_summary', False)])
    posted = len([t for t in tweets.values() if t.get('is_about_hp', False) and t.get('is_in_summary', False)])
    return render_template('alltweets.html',
                           tweets=tweets,
                           count=count,
                           excluded=excluded,
                           not_posted=not_posted,
                           posted=posted)


class IncludeKeywordForm(Form):
    ikeyword = StringField('ikeyword', validators=[DataRequired()])


class ExcludeKeywordForm(Form):
    ekeyword = StringField('ekeyword', validators=[DataRequired()])


def apply_keyword(match, *, include=False, exclude=False):
    assert sum([include, exclude]) == 1
    tweets = get_existing_tweets()
    for t_id, tweet in tweets.items():
        # Skip tweets that already have this attribute set
        if 'is_about_hp' in tweet:
            continue

        if match.lower() in tweet['text'].lower():
            if include:
                tweet['is_about_hp'] = True
            elif exclude:
                tweet['is_about_hp'] = False

    write_tweets(tweets)


@app.route('/keywords', methods=['GET', 'POST'])
def keywords_page():
    incl_form = IncludeKeywordForm()
    excl_form = ExcludeKeywordForm()

    if incl_form.validate_on_submit():
        t = incl_form.ikeyword.data
        print("Applying include to %r" % t)
        apply_keyword(t, include=True)

    if excl_form.validate_on_submit():
        t = excl_form.ekeyword.data
        print("Applying exclude to %r" % t)
        apply_keyword(t, exclude=True)

    return render_template('keywords.html',
                           incl_form=incl_form,
                           excl_form=excl_form)


@app.route('/batch', methods=['POST'])
def batch_result():
    r = request.args
    tweets = get_existing_tweets()
    if r['action'] == 'thumbsDown':
        print("Marking tweet %s as not about HP" % r['id'])
        tweets[r['id']]['is_about_hp'] = False
    elif r['action'] == 'thumbsUp':
        print("Marking tweet %s as about HP" % r['id'])
        tweets[r['id']]['is_about_hp'] = True
    elif r['action'] == 'greenTick':
        print("Marking tweet %s as in the summary" % r['id'])
        tweets[r['id']]['is_in_summary'] = not tweets[r['id']].get('is_in_summary', False)
    elif r['action'] == 'doubleThumbsDown':
        ref_d = tweets[r['id']]['date']
        print("Marking tweets before %s as about HP" % r['id'])
        for t in tweets.values():
            if 'is_about_hp' not in t and t['date'] <= ref_d:
                t['is_about_hp'] = False
    elif r['action'] == 'doubleThumbsUp':
        print("Marking tweets after %s as not about HP" % r['id'])
        ref_d = tweets[r['id']]['date']
        for t in tweets.values():
            if 'is_about_hp' not in t and t['date'] <= ref_d:
                t['is_about_hp'] = True

    write_tweets(tweets)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')