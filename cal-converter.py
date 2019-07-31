import csv
from dateutil.parser import *
from datetime import datetime
from datetime import timedelta

dates = []
with open('July29.csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    flag = 0
    name = 'John Luetzelschwab'
    valid_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    cal_days = {'Monday':'','Tuesday':'','Wednesday':'','Thursday':'','Friday':''}
    for day in valid_days: #checks for all the days
        for row in reader: #locates the row of the selected employee
            if day in row['Name']: #first name of 'day' found
                dates.append(row['Name'])
                flag = 1
            if flag == 1 and row['Name'] == name: #if name found --> save dict object and break!
                day_info = row
                break
            if flag == 1 and row['Name'] == '': #invalid info given, last name of 'sday' found
                flag = 0
        
        cal_days[day] = day_info #save the day's info into a dict


new_dates = []
for date in dates: #converting dates[str] to new_dates[datetime]
    date = date + ' 2019' #NOTE: Only works for 2019!
    new_dates.append(datetime.strptime(date,'%A, %B %d %Y'))


    
with open('ex_cal.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Subject','Start Date','Start Time','End Date','End Time']) #cal object headers

    for day, date in zip(cal_days,new_dates):
        #writer.writerow(day) NOTE: Debug headers
        strdate = date.strftime('%m/%d/%y') #convert date to datetime
        today8am = parse('8:00 AM')
        for time, shift in cal_days[day].items():
            try:
                time = parse(time) #convert times to...datetimes
                time = time.replace(microsecond=0)
            except:
                pass

            if time == '': #end after 5
                break
            if shift != '' and shift != 'a' and shift != name:
                if time < today8am: #if time < 8am assume you mean afternoon, add 12 hours
                    time = time + timedelta(hours=12)
                strtime = time.strftime('%H:%M%S')
                strtime_end = (time+timedelta(minutes=30)).strftime('%H:%M%S')
                writer.writerow([shift, strdate, strtime[:-2], strdate, strtime_end[:-2]]) #write to csv