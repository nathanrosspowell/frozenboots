from datetime import datetime
from pytz import timezone
import time

def get_time_zone():
    if time.daylight:
        return time.tzname[ 1 ]
    return time.tzname[ 0 ] 

def get_w3c_date( split_results = None ):
    now = datetime.now()
    date = datetime( 
        now.year,
        now.month,
        now.day, 
        now.hour, 
        now.minute, 
        now.second, 
        tzinfo=timezone("UTC") 
    ).isoformat( 'T' ) 
    if time.daylight:
        offset = time.altzone / 60.0 / -60.0
        offset = "+%05.2f" % offset if offset > 0 else "%06.2f" % offset  
        tz = offset.replace( ".", ":" )
    else:
        tz = timezone( time.tzname[ 0 ] ).localize( now ).strftime('%z')
        tz = tz[:-2] + ":" + tz[-2:]
    date = date[ : -6 ] + tz
    if split_results:
        return date, date[ :-6], tz
    return date

def get_gmt_time():
    full_date, date, tz = get_w3c_date( True )
    years = date[ :11 ]
    time = date[ 11: ]
    hours = int( time[ :2 ] )
    mins = int( time[ 3:5 ] ) 
    hours -= int( tz[ :3 ] )
    if hours < 0:
        hours += 24
    elif hours >= 24:
        hours -= 24
    mins -= int( tz[ 4:6 ] )
    if mins < 0:
        mins += 60
    if mins >= 60:
        mins -= 60
    time2 = "%02d:%02d:%s" % ( hours, mins, time[ 6: ] )
    return time2

if __name__ == "__main__":
    print get_w3c_date()
    print get_gmt_time()
