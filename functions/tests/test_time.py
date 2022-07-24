from functions.time import getTimeDiff
import datetime

def test_getTimeDiff():
    match = {'start_time': datetime.datetime.timestamp(datetime.datetime.now())-4200, 'duration': 1000}
    time_match = getTimeDiff(match)
    assert(time_match['time_difference'].split(".")[0] == '0:53:20')

