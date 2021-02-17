from datetime import datetime
from dateutil import tz

def UtcToLocal(utc):
    return utc.astimezone(tz.tzlocal());

def LocalToUtc(local):
    return local.astimezone(tz.tzutc());