import datetime
import dateutil.parser

def get_date(d):
    "Takes one arg, which should be something representing a date"
    if isinstance(d, datetime.date):
        return d
    elif isinstance(d, datetime.datetime):
        return d.date()
    else:
        return parsedate(d).date()

def get_range(d):
    """
    Takes a dictionary. Needs keys for start and/or end. 
    Will produce defaults if neither.
    """
    DEFAULT_RANGE = 30
    start = d.get('start', None)
    end = d.get('end', None)
    
    if end:
        end_date = get_date(end)
    else:
        try:
            end_date = SmogUpdate.objects.latest().timestamp
        except:
            end_date = datetime.datetime.now() + datetime.timedelta(.5)
    
    if start:
        start_date = get_date(start)
    else:
        start_date = end_date - datetime.timedelta(DEFAULT_RANGE)
    
    return start_date, end_date


def parsedate(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    dt = dateutil.parser.parse(s)
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt
