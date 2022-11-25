# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import calendar
from datetime import date
from nsepython import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
from time import strptime
import requests
import json
import pandas as pd
from .models import *

def numtomon(num):
    months=[        'Jan',
        'Feb', 
        'Mar', 
        'Apr', 
        'May', 
        'Jun', 
        'Jul', 
        'Aug', 
        'Sep', 
        'Oct',
        'Nov', 
        'Dec']
    return months[num-1]


def expiry_list_gen():
    sdate = datetime.date(datetime.now())  # start date
    edate = date(2023, 12, 31) 
    types='03-Nov-2022'
    expiry_list=[]
    while sdate < edate:
        if sdate.weekday() != 3:  # not thursday
            sdate += timedelta(days=1)
            continue
        # It is thursday
        if (len(str(sdate.day))==1):
            date1='0'+str(sdate.day)

        else:
            date1=sdate.day
        expiry_list.append(str(date1)+'-'+numtomon(int(sdate.month))+"-"+str(sdate.year))
        print(sdate.month)
        sdate += timedelta(days=7)  #  next week

    return expiry_list



def this_scripts():

    url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    print(url)
    data=requests.get(url=url)
    print(url)
    data=data.json()
    df = pd.DataFrame(data)

    # df=pd.read_csv('datamanagement/scripts.csv')

    df1=df[:1]
    # print(df1)


    for i in range(len(df)):
        print(i)

        if 'NIFTY' in df['symbol'][i][:6] and 'NFO' in df['exch_seg'][i]:
            df1.loc[len(df1.index)] = df.loc[i] 
        else:
            continue
    # print(df)

    df1.to_csv("datamanagement/scripts.csv")


def monthToNum(shortMonth):
    return {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }[shortMonth]

def numtomon(num):
    months=[        'jan',
        'feb', 
        'mar', 
        'apr', 
        'may', 
        'jun', 
        'jul', 
        'aug', 
        'sep', 
        'oct',
        'nov', 
        'dec']
    return months[num-1]

data_holiday=[{'tradingDate': '26-Jan-2022', 'weekDay': 'Wednesday', 'description': 'Republic Day', 'Sr_no': 1}, {'tradingDate': '01-Mar-2022', 'weekDay': 'Tuesday', 'description': 'Mahashivratri', 'Sr_no': 2}, {'tradingDate': '18-Mar-2022', 'weekDay': 'Friday', 'description': 'Holi', 'Sr_no': 3}, {'tradingDate': '10-Apr-2022', 'weekDay': 'Sunday', 'description': 'Ram Navami', 'Sr_no': 4}, {'tradingDate': '14-Apr-2022', 'weekDay': 'Thursday', 'description': 'Dr.Baba Saheb Ambedkar Jayanti/Mahavir Jayanti', 'Sr_no': 5}, {'tradingDate': '15-Apr-2022', 'weekDay': 'Friday', 'description': 'Good Friday', 'Sr_no': 6}, {'tradingDate': '01-May-2022', 'weekDay': 'Sunday', 'description': 'Maharashtra Day', 'Sr_no': 7}, {'tradingDate': '03-May-2022', 'weekDay': 'Tuesday', 'description': 'Id-Ul-Fitr (Ramzan ID)', 'Sr_no': 8}, {'tradingDate': '10-Jul-2022', 'weekDay': 'Sunday', 'description': 'Bakri Id', 'Sr_no': 9}, {'tradingDate': '09-Aug-2022', 'weekDay': 'Tuesday', 'description': 'Moharram', 'Sr_no': 10}, {'tradingDate': '15-Aug-2022', 'weekDay': 'Monday', 'description': 'Independence Day', 'Sr_no': 11}, {'tradingDate': '31-Aug-2022', 'weekDay': 'Wednesday', 'description': 'Ganesh Chaturthi', 'Sr_no': 12}, {'tradingDate': '02-Oct-2022', 'weekDay': 'Sunday', 'description': 'Mahatma Gandhi Jayanti', 'Sr_no': 13}, {'tradingDate': '05-Oct-2022', 'weekDay': 'Wednesday', 'description': 'Dussehra', 'Sr_no': 14}, {'tradingDate': '24-Oct-2022', 'weekDay': 'Monday', 'description': 'Diwali * Laxmi Pujan', 'Sr_no': 15}, {'tradingDate': '26-Oct-2022', 'weekDay': 'Wednesday', 'description': 'Diwali-Balipratipada', 'Sr_no': 16}, {'tradingDate': '08-Nov-2022', 'weekDay': 'Tuesday', 'description': 'Gurunanak Jayanti', 'Sr_no': 17}, {'tradingDate': '25-Dec-2022', 'weekDay': 'Sunday', 'description': 'Christmas', 'Sr_no': 18}]

def getting_holidays():
    print("bro")
    Year = datetime.now().year
    A = calendar.TextCalendar(calendar.SUNDAY)
    B = calendar.TextCalendar(calendar.SATURDAY)

    holiday = pd.json_normalize(data_holiday)

    holidays = []

    for b in range(1, 13):
        for k in A.itermonthdays(Year, b):
            if k != 0:
                day = date(Year, b, k)
                if day.weekday() == 6:
                    # print("%d-%d-%d" % (k,b,Year))
                    holidays.append(str(k)+'-'+str(b)+'-'+str(Year)[-2:])

    for b in range(1, 13):
        for k in B.itermonthdays(Year, b):
            if k != 0:
                day = date(Year, b, k)
                if day.weekday() == 5:
                    # print("%d-%d-%d" % (k,b,Year))
                    holidays.append(str(k)+'-'+str(b)+'-'+str(Year)[-2:])

    holiday_list = list(holiday['tradingDate'])

    for i in range(len(holiday_list)):
        month = holiday_list[i][3:6]
        month = strptime(str(month), '%b').tm_mon
        holidays.append(holiday_list[i][:3]+str(month)+'-'+holiday_list[i][9:])

    return holidays


def expiry_dates():
    expiry_dates = []
    with open('datamanagement/option_chain_scrape.json') as json_file:
        data_option_scrape = json.load(json_file)
    payload = data_option_scrape

    for i in range(1000):
        try:
            currentExpiry, dte = nse_expirydetails(payload, i)
            expiry_dates.append(str(currentExpiry)[2:])

        except:
            return expiry_dates


def convert_to_datetime(holidays, expiry):

    holiday_datetime = []
    expiry_datetime = []

    for i in range(len(holidays)):
        date_time_obj = datetime.strptime(holidays[i], '%d-%m-%y')

        holiday_datetime.append(date_time_obj)

    for i in range(len(expiry)):
        date_time_obj = datetime.strptime(expiry[i], '%y-%m-%d')

        expiry_datetime.append(date_time_obj)

    return holiday_datetime, expiry_datetime


def working_days(expiry_date, holidays):
    current = datetime.now()
    # print(expiry_date)
    difference = expiry_date-current+timedelta(days=1)
    # print(difference)
    for i in range(len(holidays)):
        if holidays[i] > current and holidays[i] < expiry_date:
            difference -= timedelta(days=1)

    return difference.days



def expiry_list_gen_1():
    sdate = datetime.date(datetime.now())  # start date
    edate = date(2023, 12, 31) 
    types='03-Nov-2022'
    expiry_list=[]
    while sdate < edate:
        if sdate.weekday() != 3:  # not thursday
            sdate += timedelta(days=1)
            continue
        # It is thursday
        if (len(str(sdate.day))==1):
            date1='0'+str(sdate.day)

        else:
            date1=sdate.day
        expiry_list.append(str(sdate)[2:])
        
        sdate += timedelta(days=7)  #  next week

    
    return expiry_list

def working_day_calculation(value):
    print("doing it brooo....")
    this_scripts()

    holidays = getting_holidays()
    print("got holidays")
    expiry = expiry_list_gen_1()


    holiday_date, expiry_date = convert_to_datetime(holidays, expiry)
    days_1 = working_days(expiry_date[0], holiday_date)
    days_2 = working_days(expiry_date[1], holiday_date)
    days_3 = working_days(expiry_date[2], holiday_date)
    print("got expiry dates")
    expiry_nifty=expiry_list_gen()



    print("got expiry list")
    expiry_1=option_symbol('NIFTY',expiry_nifty[0])
    expiry_2=option_symbol('NIFTY',expiry_nifty[1])
    expiry_3=option_symbol('NIFTY',expiry_nifty[2])
    
    # expiry_2=option_symbol('NIFTY',)

    print("option symbols")
    user=User1.objects.get(username='testing')
    

    user.working_days_1=int(days_1)
    user.working_days_2=int(days_2)
    user.working_days_3=int(days_3)
    user.expiry_1=expiry_1
    user.expiry_2=expiry_2
    user.expiry_3=expiry_3
    print(expiry_1, expiry_2,expiry_3)
    print("#####################################")
    user.save()
    print("done it brooo....")
    return days_1,days_2


# %%
def option_symbol(symbol, expiry_date):
    return str(symbol)+str(expiry_date[:2])+str(expiry_date[3:6]).upper()+expiry_date[-2:]


