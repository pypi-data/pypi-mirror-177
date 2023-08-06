from datetime import datetime as dt, timedelta as td
from datetime import datetime
from xmlrpc.client import DateTime


# COLOCANDO AQUI FICA GENERICO E VOCE PODE PASSAR PARA OUTROS PROJETOS

class DateUteis():
    def now(fmt=None):
        v =  dt.now()
        return v if not fmt else v.strftime(fmt)

    def getDateRange(startAt=None,days=0,fmt=None):
        today = DateUteis.today() #
        dates = []

        if days >= 0:
            dates = [DateUteis.dateAddDays(today,x,fmt=fmt) for x in range(0, days)]
        else:
            dates = [DateUteis.dateAddDays(today,x*-1,fmt=fmt) for x in range(0, abs(days))]
        return dates 

    def today(fmt=None,addDays=0):
        v =  dt.now().date() 
        v =  v if not addDays else DateUteis.dateAddDays(v,addDays)
        return v if not fmt else v.strftime(fmt)

    def yesterday(fmt=None):
        v = dt.now() - td(1)
        return v if not fmt else v.strftime(fmt)

    def dateAddDays(date:datetime,days:int,fmt=None):
        v = date + td(days) if days > 0 else date - td(abs(days))
        return v if not fmt else v.strftime(fmt)

    def lastWorkingDate(ref:datetime=None,fmt=None): #IGNORE MONDAY AND SUNDAY
        self = DateUteis
        y = self.yesterday() if not ref else self.dateAddDays(ref,-1)
        if y.weekday() in [5,6]:
            return self.lastWorkingDate(self.dateAddDays(y,-1),fmt)
        return y if not fmt else y.strftime(fmt)
    

# d = DateUteis()
# a = d.lastWorkingDate(fmt="%Y-%m-%d")
# a=1
