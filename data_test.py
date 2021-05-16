import datetime
now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year
hour = now.hour
minute = now.minute
second = now.second
microsecond = now.microsecond

while True:
    now = datetime.datetime.now()
    data = (str(now.day-day)+':'+str(now.month-month)+':'+str(now.year-year))
    time = (str(now.hour-hour)+':'+str(now.minute-minute)+':'+str(now.second-second)+':'+str(now.microsecond-microsecond))


    print(data + ' ' + time)