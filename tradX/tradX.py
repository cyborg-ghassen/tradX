from datetime import datetime
import websocket, json, pprint, talib, numpy
import config, time, sys
from binance.client import Client
from binance.enums import *
from telethon.sync import TelegramClient

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'BTCUSD'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='com')


api_id = yourtelegramapiid
api_hash = 'yourtelegramapihash'
phone = '+216yourphonenumber'
username = "yourtelegramusername"
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    c = 0
    d = 0
    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        client.send_message(username, "selled {} of {}".format(TRADE_QUANTITY, TRADE_SYMBOL))
                        c += TRADE_QUANTITY
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        d += TRADE_QUANTITY
                        client.send_message(username, "buyed {} of {}".format(TRADE_QUANTITY, TRADE_SYMBOL))
                        in_position = True

    while True:
        client.send_message(username, "Buyed quantity is: {}BTC\nSelled quantity is: {}BTC\nDifferece: {}BTC".format(d, c, c - d))
        time.sleep(86400)

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
