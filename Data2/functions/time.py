import datetime

def getTimeDiff(match):
  unix_time = match['start_time'] + match['duration']
  date_time = datetime.datetime.fromtimestamp(unix_time)
  today = datetime.datetime.now()
  match['time_difference'] = str(today-date_time)
  return match