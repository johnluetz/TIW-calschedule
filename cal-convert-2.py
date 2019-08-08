#the better version!
import csv
from datetime import datetime
from dateutil.parser import *
from shift import Shift

dates = []
#name = 'John Luetzelschwab'
name = 'Kolbe Bauer'
with open('July29.csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    flag = 0
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
            if flag == 1 and row['Name'] == '': #invalid info given, last name of 'day' found
                flag = 0
        
        cal_days[day] = day_info #save the day's info into a dict


for day in cal_days: #cleans up dict, removes name & ''
    del (cal_days[day])['Name']
    del (cal_days[day])['']

now = datetime.now()
for x in range(len(dates)): #cleans up dates, adds the current year
    date_time = parse(dates[x] +" "+ str(now.year))
    dates[x] = date_time.strftime('%m/%d/%Y')



#opens the new Cal CSV file..
with open('ex_cal.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Subject','Start Date','Start Time','End Date','End Time']) #cal object headers

    #structured as a dictionary of days containing a list of Shift objects
    shift_list = {'Monday':'','Tuesday':'','Wednesday':'','Thursday':'','Friday':''}
    date_cnt = 0 #handles the current date to write to the output    
    for day in cal_days: #creates the schedule
        shifts = []
        times = []
        for key in cal_days[day]: #converts dict to two lists...because
            times.append(key)
            shifts.append((cal_days[day])[key])
        #print(times)
        #print(shifts)


        length = len(times)
        shift_info = {'Name':'','Start':'','End':''}
        shift_list = []

        #finds all shifts per day and adds to a Shift object
        for index in enumerate(times):
            this_shift = shifts[index[0]]
            this_time = times[index[0]]

            if(shift_info['Name'] == '' and this_shift != '' and this_shift != 'a'): #start a new shift 
                shift_info['Name'] = this_shift
                shift_info['Start'] = this_time

            if(shift_info['Name'] != this_shift and this_shift != 'a'): #the shift ended
                shift_info['End'] = this_time
                shift_block = Shift(shift_info['Name'],shift_info['Start'],shift_info['End']) #create a new shift object & append
                shift_list.append(shift_block)
                shift_info['Name'] = this_shift
                shift_info['Start'] = this_time

        #cleans up the last shift
        if(this_time == '5:00' and shift_info['Name'] != this_shift): #if ends at 5
            shift_info['End'] = '5:00'
            shift_block = Shift(shift_info['Name'],shift_info['Start'],shift_info['End']) #create a new shift object & append
            shift_list.append(shift_block)
        elif(this_time == '5:00' and this_shift != '' and this_shift != 'a'): #if ends at 5:30
            shift_info['End'] = '5:30'
            shift_block = Shift(shift_info['Name'],shift_info['Start'],shift_info['End']) #create a new shift object & append
            shift_list.append(shift_block)

        print(dates[date_cnt])
        for shift in shift_list:
            
            print(str(shift))
            writer.writerow([shift.shift, dates[date_cnt], shift.start_time, dates[date_cnt], shift.end_time]) #write to csv
        date_cnt = date_cnt + 1
        

        
    






    
