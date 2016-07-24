# jkr-tweetr

This is a collection of scripts/data I was using to help me compile a
list of [@jk_rowling](https://twitter.com/jk_rowling)'s tweets about
Harry Potter, for an answer on the [Sci-Fi & Fantasy Stack Exchange][sff].

## Why am I posting this?

I won't be maintaining that answer any longer.  I don't have the time:

*   I've steadily drifted away from the SFF Stack Exchange, and it gets
    virtually none of my free time these days.
*   I don't have much bandwidth right now, and I'm cutting loose ends.
*   I'm not super comfortable with some of the latest Pottermore updates/tweets,
    e.g. with regard to native American culture, and running this project was
    causing more angst than it was worth.

Perhaps something here will be useful, but I make no guarantees.  I'm not
going to be suppporting or helping anybody use this code, and any requests
for the above will be ignored.

## What's in the repo?

This code is in a very rough state, pretty much the first hacked-together
version that I wrote.

There are three interesting files:

*   `jk_rowling.json` -- a data file containing a collection of tweets.  Each
    tweet has a couple of attributes:

    *   `text`, `url`, `date` (self-explanatory)
    *   `is_about_hp`: true/false (is the tweet about Harry Potter)
    *   `is_in_summary`: true/false (has the tweet been included in my
        summary post)

*   `fetch_tweets.py` -- given a set of Twitter API credentials, grab the
    latest tweets from JK Rowling and add them to `jk_rowling.json`.

*   `are_tweets_about_hp.py` -- this serves a simple Flask app that I was
    using to batch process tweets.  Each tweet had five buttons:

    ![](buttons.png)

    *   👍 = tweet is about Harry Potter
    *   👎 = tweet is not about Harry Potter
    *   ✅ = tweet has been included in the summary post

    with colour coding to match.  The 👍👍 and 👎👎 buttons were for bulk
    updates: they would apply the rating not just to that tweet, but to every
    older tweet that didn't already have a rating.

## Installation

Requires Python&nbsp;3, plus the following third-party packages (`pip install`):

*   dateutil
*   flask, flask-wtf
*   keyring
*   tweepy

You'll need to set up some Twitter API credentials in the local keychain --
look at the `setup_api()` method for guidance.

## License

Scripts are [Creative Commons Zero][cc0].  Data file is all JK Rowling's
tweets, so whatever license Twitter uses.

[cc0]: https://creativecommons.org/publicdomain/zero/1.0/
[sff]: http://scifi.stackexchange.com/a/121214/3567