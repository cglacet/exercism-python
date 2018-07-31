from datetime import datetime, timedelta

GIGASECONDS_TIMEDELTA = timedelta(seconds=10**9)

def add_gigasecond(birth_date):
    return birth_date + GIGASECONDS_TIMEDELTA
