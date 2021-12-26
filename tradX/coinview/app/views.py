"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .config import *
import datetime
from binance.client import Client
from binance.enums import *
from django.contrib.auth.decorators import login_required

client = Client(API_KEY, API_SECRET, tld='com')

@login_required
def home(request):
    title = 'TradX'

    status = client.get_account_status()['data']
    timezone, time = client.get_exchange_info()['timezone'], client.get_exchange_info()['serverTime']
    account = client.get_account()
    orders = client.get_open_orders()

    balances = account['balances']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render(request, 'index.html', {
        'title': title, 
        'my_balances': balances, 
        'symbols': symbols,
        'status': status,
        'time':  datetime.datetime.now(),
        'orders': orders
        } )

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def history(request):
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Dec, 2021", "31 Dec, 2022")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return JsonResponse(processed_candlesticks, safe=False)