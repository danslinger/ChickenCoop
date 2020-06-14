import requests
from crontab import CronTab 
import json
import datetime 
from dateutil import parser, tz
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
SUNRISE_DELTA = 45
SUNSET_DELTA = 30


def getLocalDateTime(dateString):
    d = parser.parse(dateString)
    d = d.replace(tzinfo=tz.tzutc())
    return d.astimezone(tz.tzlocal())

def getJob(cron, comment):
    jobs = [job for job in cron.find_comment(comment)]
    if jobs:
        return jobs[0]
    else:
        return None

def getSunData():
    url = 'http://api.sunrise-sunset.org/json'
    payload = { 'lat': '45.59',
                'lng': '-121.17',
                'formatted': '0'
              }
    r = requests.get(url, params=payload)
    data =r.json()
    return data

def setSunJobs(cron, data, sunriseJob, sunsetJob):
    localSunrise = getLocalDateTime(data['results']['sunrise'])
    localSunset = getLocalDateTime(data['results']['sunset'])

    # Passing in the .time() value makes it so the date isn't included in the cron
    # This is important if the update fails, then the cron will still run on the previous day's schedule.
    sunriseJobTime = (localSunrise + datetime.timedelta(minutes=SUNRISE_DELTA)).time()
    sunsetJobTime = (localSunset+ datetime.timedelta(minutes=SUNSET_DELTA)).time() 


    sunriseJob.setall(sunriseJobTime)
    sunsetJob.setall(sunsetJobTime)
    cron.write()
    return sunriseJobTime, sunsetJobTime

def main(cron):
    logging.basicConfig(filename="/home/pi/doorLog.log",format='%(asctime)s:%(message)s', level=logging.DEBUG)
    sunriseJob = getJob(cron, "SUNRISE") or cron.new(command='sudo python /home/pi/Door/openDoor.py', comment="SUNRISE")
    sunsestJob = getJob(cron, "SUNSET") or cron.new(command='sudo python /home/pi/Door/closeDoor.py', comment="SUNSET")
    data = getSunData()
    doTime, dcTime = setSunJobs(cron, data, sunriseJob, sunsestJob)
    logging.info("Updated Cron Jobs\n\t\t\tOpen Door at " + str(doTime) + "\n\t\t\tClose Door at " + str(dcTime))


if __name__ == '__main__':
    main(CronTab(user=True))




