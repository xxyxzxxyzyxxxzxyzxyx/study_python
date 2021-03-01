import calendar
from datetime import date, timedelta

class DST(object):
    def __init__(self, year):
        self.year = year
        self.dwdict = {
            'mon': 0,
            'tue': 1, 
            'wed': 2, 
            'thu': 3, 
            'fri': 4, 
            'sat': 5,
            'sun': 6
        }
        self.whatdwdict = {
            'first' :  0,
            'second':  1,
            'last'  : -1
        }

    
    def whatdwdate(self, month, dw, whatdw):
        lastday = calendar.monthrange(self.year, month)[1]
        targedw = self.dwdict[dw.lower()[0:3]]
        dwlist = []
        for i in range(1, lastday+1):
            if date(self.year, month, i).weekday() == targetdw:
                dwlist.append(i)
            else:
                pass
            
        return date(self.year, month, dwlist[self.whatdwdict[whatdw.lower()]])

    
    def newyork(self):
        if self.year <= 2006:
            return self.whatdwdate(4, 'sunday', 'first'), self.whatdwdate(10, 'sunday', 'last')
        else:
            return self.whatdwdate(3, 'sunday', 'second'), self.whatdwdate(11, 'sunday', 'first')