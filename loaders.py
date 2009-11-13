import datetime
import dateutil.parser
import urllib, urllib2

try:
    import json
except ImportError:
    import simplejson as json

from decimal import Decimal
from django.db import transaction
from beijing_air.models import SmogUpdate, AqiDefinition


BASE_URL = "http://twitter.com/statuses/user_timeline.json?"

def get_tweets(**params):
    response = urllib2.urlopen(BASE_URL + urllib.urlencode(params)).read()
    return json.loads(response)


def parsedate(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    dt = dateutil.parser.parse(s)
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt


@transaction.commit_on_success
def update(**params):
    """
    Imports updates from BeijingAir twitter feed.
    Since the feed is updated automatically, we can 
    assume old tweets won't be updated. So, we'll just
    check when the last update was, and use since_id to
    get tweets after that.

    We'll also lock in the BeijingAir twitter name.
    """
    try:
        latest_update = SmogUpdate.objects.order_by('-tweet_timestamp')[0]
        params['since_id'] = long(latest_update.tweet_id)
    except IndexError:
        latest_update = None
        params['count'] = 200 # no updates yet, so get the max

    params['screen_name'] = 'BeijingAir'

    tweets = get_tweets(**params)

    for tweet in tweets:
        tweet_list = tweet['text'].split(' ; ')
        update = SmogUpdate()
        update.timestamp = datetime.datetime.strptime(tweet_list[0] + tweet_list[1], '%m-%d-%Y%H:%M')
        update.concentration = tweet_list[3]
        update.aqi = tweet_list[4]

        try:
            d = AqiDefinition.objects.get(name__iexact=tweet_list[5])
        except AqiDefinition.DoesNotExist:
            d = update.check_definition

        update.definition = d

        update.tweet_id = str(tweet['id'])
        update.tweet_timestamp = parsedate(tweet['created_at'])

        update.save()
