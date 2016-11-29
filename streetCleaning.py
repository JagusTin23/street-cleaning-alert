#!/usr/bin/python3.5
# This script alerts a user of upcoming street cleaning days via text.  
# Uses Twilio API for texting. 
# Is meant to be run as a scheduled task via launch or cron on Unix/Linux OS.  
# A logs.txt file should be created and saved in the current wroking directory
# prior to running the program with a single date writen on it in the format 
# Year-Month-Day e.g. 2016-10-11.  

import datetime
from datetime import timedelta
import time
import sys
from twilio.rest import TwilioRestClient

tdy = datetime.datetime.now()
t_start = tdy.strftime("%Y-%m-%d")

# Only run if current day is Monday.  
if tdy.isoweekday() != 1:
    sys.exit(None)

with open('./logs.txt') as f: 
    tlog = f.read().split()[0]
    if tlog == t_start:
        sys.exit(None)
    
# Iterates through the days of the month and determines if a day falls in 
# a particular day of the month (e.g. first and third tuesday of the month).  
def get_n_weekday(year, month, day_of_week, n):
    count = 0
    for i in range(1, 32):
        try:
            d = datetime.date(year, month, i)
        except ValueError:
            break
        if d.isoweekday() == day_of_week:
            count += 1
        if count == n:
            return d
    return None

# A list containing current date with YMD numbers stored as individual objects.  
sDay = [int(_) for _ in t_start.split("-")]

# To append with first and third Tuesday and Fridays of the month.  
street_cleaning_days = []

# Interested in Tuesday (2) and Friday (5)
daysToChK = [2, 5]

# First and third days of the month
nth_days = [1, 3]

# Get all 1st and 3rd Tuesdays and Fridays of current month. 
for dy in daysToChK:
    for nth_day in nth_days:
        street_cleaning = get_n_weekday(sDay[0], sDay[1], dy, nth_day)
        street_cleaning_days += [str(street_cleaning)]

# Get all 1st and 3rd Tuesdays and Fridays of the following month
if sDay[1] + 1 <= 12:
    for dy in daysToChK:
        for nth_day in nth_days:
            street_cleaning = get_n_weekday(sDay[0], sDay[1] + 1, dy, nth_day)
            street_cleaning_days += [str(street_cleaning)]
else:
    for dy in daysToChK:
        for nth_day in nth_days:
            street_cleaning = get_n_weekday(sDay[0] + 1, 1, dy, nth_day)
            street_cleaning_days += [str(street_cleaning)]

# Get dates of coming Tuesday and Friday.
tues = (tdy + timedelta(days = 1)).strftime("%Y-%m-%d")
fri = (tdy + timedelta(days = 4)).strftime("%Y-%m-%d")

daysToMove = []

# Appends daysToMove if Tues and Fri of current week are in street_cleaning_days.
# Date formated e.g. "Tuesday 10/18" to print on text body.
for day in [tues, fri]:
    if day in street_cleaning_days:
        day = datetime.datetime.strptime(day, "%Y-%m-%d")
        daysToMove += [str(day.strftime("%A"))+" "+str(day.strftime("%m-%d"))]

# Exists if no days are in daysToMove.  
if len(daysToMove) == 0:
    sys.exit(None)

if len(daysToMove) == 1: 
    fbody = "Aloha! Street cleaning happens this week on {}.".format(daysToMove[0]) \
    + " Make sure to move your car ;)"

elif len(daysToMove) == 2:
    fbody = "Aloha! Street cleaning happens this week on {} and {}.".format(daysToMove[0], 
    daysToMove[1]) + " Make sure to move your car ;)"

# Twilio account info.  
client = TwilioRestClient(account = "YOUR-TWILIO-ACCOUNT-NUMBER",
                            token = "YOUR-TWILIO-TOKEN")

# Numbers to text street cleaning alerts.  
numbers = ['(888) 888-8888', '(888) 888-8888']

for number in numbers:
    client.messages.create(from_='YOUR-TWILIO-NUMBER',
                       to= number,
                       body= fbody)

with open('./logs.txt', "w") as logs:
    logs.write(str(tdy))
