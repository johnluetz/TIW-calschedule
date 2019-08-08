#Shift
from dateutil.parser import *
from datetime import datetime
from datetime import timedelta

class Shift:
    def __init__(self, shift, start_time, end_time):
        self.shift = shift
        self.start_time = convert(start_time)
        self.end_time = convert(end_time)
    
    def __str__(self):
        return(self.start_time+"-"+self.end_time+" "+self.shift)
    
#converts the given time to AM/PM...only works for certain times during limited hours. Fix it by updating the spreadsheet to include AM/PM.
def convert(str_time):
    time = parse(str_time)
    today8am = parse('8:00 AM')
    if time < today8am: #if time < 8am assume you mean afternoon, add 12 hours
                time = time + timedelta(hours=12)
    return(time.strftime('%H:%M'))

        

