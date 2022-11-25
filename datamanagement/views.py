import logging
import telepot
from datamanagement.background_functions import working_days
from django.shortcuts import redirect, render
from .data_collection import run_strategy as collect_data
from .strategy import *
from ast import literal_eval
from django.contrib.auth import authenticate,  login, logout
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import threading
from datamanagement.models import strategy
import random
import json
import string
from .models import positions, orders, strategy
from .background_functions import *
from smartapi import SmartConnect
import yfinance as yf
import time as tim
import ccxt
from datetime import time, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from AesEverywhere import aes256
# working_day_calculation(0)
logger = logging.getLogger('dev_log')
sleep_time=0

def get_app_session_id():
    url="https://stagingtradingorestapi.swastika.co.in/auth/SSO/GetSSOAppSessionId"
    body = {
            "AccessKey": "LAKSGPT@APK1734#",
            "AccessSecret": "AFE2253F-5A4F-4590-BA13-F69B3D8B5E10"
            }

    response=requests.get(url,data=body).json()
    
    user=User1.objects.get(username="testing")
    user.app_session_id_url=f'https://stagingjustradekb.swastika.co.in/auth/login?AppSessionId={response["Data"]["AppSessionId"]}&State=SWASTIKA'
    logger.info(f"SESSION CREATED BY CLIENT - {user.app_session_id_url}")
    user.save()


@api_view(["POST","GET"]) #allowed methods
def get_session_id(request):
    data=request.data
    access_token=aes256.decrypt(request.data['ReturnParameter'], '9E5000F4-6489-4D84-8B67-B8D8D481F9BB')
    access_token=literal_eval(access_token.decode('utf-8'))
    client_code=access_token['ClientCode']
    access_token=access_token['AccessToken']
    user=User1.objects.get(username="testing")
    user.access_token=access_token
    user.client_code=client_code
    user.save()

    return Response(data)




@login_required(login_url='')
def index(request):
    with open('datamanagement/data.json') as data_file:
        data = json.load(data_file)

    df=yf.download("^NSEI",period='1d',interval='1d')

    user=User1.objects.get(username="testing")
    # user.app_session_id_url="https://stackoverflow.com/questions/2906582/how-do-i-create-an-html-button-that-acts-like-a-link"
    return render(request, "index.html",{
        "nifty":round(df['Close'][-1],2),
        "user":user

    })






@login_required(login_url='')
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

@login_required(login_url='')
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
        paper=request.POST['paper']
        try:
            type = str(request.POST['type'])

        except:
            type = 'off'

        rand_str = random_string_generator(10, string.ascii_letters)
        # obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
        user = User1.objects.get(username='testing')

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
            paper=paper,
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
        print(f"PAPER IS- {paper}")
        strategy1.save()

        strategy1 = strategy.objects.get(strategy_id=rand_str)
        
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

    strat = run_strategy(strategy)
    value=strat.run()
    if value!=None:
        return value



@login_required(login_url='')
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


def login_page(request):
    return render(request, "login.html")

def handleLogin(request):

    if request.user.is_authenticated:
        return redirect('/../../data/index')
    if request.method == "POST":

        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        # user = authenticate(username=loginusername, password=loginpassword)
        if loginpassword=="abcd@1234" and loginusername=="Y99521":
            user=User.objects.get(username=loginusername)
            login(request, user)
            return redirect("/../../data/index")
        else:

            messages.error(request, "Invalid credentials! Please try again")
            return redirect("accounts/login")
    return redirect("accounts/login")