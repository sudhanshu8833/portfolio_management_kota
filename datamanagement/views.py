import logging
import telepot
from datamanagement.background_functions import working_days
from django.shortcuts import redirect, render
from .data_collection import run_strategy as collect_data
from .strategy import *
# Create your views here.
from django.contrib import messages
import threading
from datamanagement.models import strategy
import random
import string
from .models import positions, orders, strategy
from .background_functions import *
from smartapi import SmartConnect
import yfinance as yf
import time as tim
import ccxt
from datetime import time, datetime
logger = logging.getLogger('dev_log')

# bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
# bot.getMe()
sleep_time=0


def do_something_1(strategy):
    check_val=0

    while True:
        try:
            if time(9, 1) <= datetime.now(timezone("Asia/Kolkata")).time() and check_val ==0:
                check_val=1
                # working_day_calculation(0)
                strat = collect_data(strategy)
                value=strat.run()
                if value!=None:
                    return value

            if time(8, 1) <= datetime.now(timezone("Asia/Kolkata")).time() and time(8, 15) >= datetime.now(timezone("Asia/Kolkata")).time() and check_val==1:
                check_val=0

            tim.sleep(600)
        except Exception as e:
            # logger.info(str(e))
            print(str(e))

# def data_calculation(request):
#     global obj




user = User1.objects.get(username='testing')

t = threading.Thread(target=do_something_1, args=[user])
t.setDaemon(True)
t.start()

    # return render(request, "index.html")


def index(request):
    with open('datamanagement/data.json') as data_file:
        data = json.load(data_file)

    df=yf.download("^NSEI",period='1d',interval='1d')
    user=User1.objects.get(username="testing")
    return render(request, "index.html",{
        "nifty":df['Close'][-1],
        "user":user
    })







def position(request):

    strategies = strategy.objects.filter(status="OPEN")
    user = User1.objects.get(username="testing")
    lists = []
    strategy_id = []

    for i in range(len(strategies)):

        position = positions.objects.filter(
            strategy_id=strategies[i].strategy_id)
        position_list = []
        for j in range(len(position)):
            position_list.append(position[j])
            print(position[j].time_in)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        lists.append(position_list)
        strategy_id.append(strategies[i])
    print(lists)
    print(strategy_id)
    return render(request, "position.html",    {
        'list': lists,
        'strategy_id': strategy_id,
        'user':user
    })


def closed_positions(request):

    strategies = strategy.objects.filter(status="CLOSED")
    lists = []
    strategy_id = [] 
    user = User1.objects.get(username="testing")

    for i in range(len(strategies)):

        position = positions.objects.filter(
            strategy_id=strategies[i].strategy_id)
        position_list = []
        for j in range(len(position)):
            position_list.append(position[j])
            print(position[j].time_in)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        lists.append(position_list)
        strategy_id.append(strategies[i])
    print(lists)
    print(strategy_id)
    return render(request, "closed_position.html",    {
        'list': lists,
        'strategy_id': strategy_id,
        'user':user
    })


def start_strategy(request):
    global sleep_time
    print(request)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    if request.method == "POST":
        print(request.POST)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        buy_factor = request.POST['buy_factor']
        per_premium = request.POST['per_premium']
        TP1 = request.POST['TP1']
        TP2 = request.POST['TP2']
        timeout = request.POST['timeout']
        sell_factor = request.POST['sell_factor']
        lot = request.POST['lot']
        et = request.POST['et']
        try:
            type = str(request.POST['type'])

        except:
            type = 'off'

        rand_str = random_string_generator(10, string.ascii_letters)
        # obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
        user = User1.objects.get(username='testing')
        user.angel_api_keys=request.POST['angel_api_keys']
        user.angel_client_id=request.POST['angel_client_id']
        user.angel_password=request.POST['angel_password']
        user.angel_token=request.POST['angel_token']
        user.save()
        print(user)
        if request.POST['action']=="review":
            status="TEST"
        else:
            status="OPEN"


        strategy1 = strategy(
            strategy_id=rand_str,
            buy_factor=buy_factor,
            sell_factor=sell_factor,
            percentage_premium=per_premium,
            TP1=TP1,
            TP2=TP2,
            time_out=timeout,
            LIMIT=type,
            lot=lot,
        

            status=status,
            ET=et,
            working_days_1=user.working_days_1,
            working_days_2=user.working_days_2,
            working_days_3=user.working_days_3,
            expiry_1=user.expiry_1,
            expiry_2=user.expiry_2,
            expiry_3=user.expiry_3,
            T_now=3

        )

        strategy1.save()

        strategy1 = strategy.objects.get(strategy_id=rand_str)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if request.POST['action']!="review":
            
            t = threading.Thread(target=do_something, args=[strategy1])
            t.setDaemon(True)
            t.start()

            return redirect("/data/position")


        else:
            data=do_something(strategy1)
            return render(request, "review_orders.html",    {
                'list': data
            })

    return render(request, "index.html")



def do_something(strategy):


    # try:
    strat = run_strategy(strategy)
    value=strat.run()
    if value!=None:
        return value

    # except Exception as e:
    #     logger.info(traceback.format_exc())


    # messages
    # while True:
    #     print(data)


def close_positions(request,strategy_id):
    strategy1 = strategy.objects.get(strategy_id=strategy_id)
    strat1 = run_strategy(strategy)
    price_buy = obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']

    v_factor = strat1.vix_calculation(price_buy)
    print(v_factor,price_buy)
    
    if strat1.parameters.expiry_selected==1:
        expiry=strat1.parameters.expiry_2

    else:
        expiry=strat1.parameters.expiry_1

    print(expiry)
    
    token_dict, dict_token=strat1.token_calculations(price_buy, v_factor, expiry)

    value=strat1.close_all_positions(token_dict,dict_token)
    return render(request, "position.html")



def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
