import os
import telebot
import requests
import time

url = "https://api.apilayer.com/exchangerates_data/latest?symbols=rub%2Camd&base=usd"

payload = {}
headers = {"apikey": "RU6c5dtyG6miALraMVauof644Y0Ds7jq"}

cur = None

def req_cur():
    res = requests.request('GET', url, headers=headers, data=payload)
    return res.json()


def update_cur():
  global cur
  if cur is None or time.time() - cur['last'] > 60 * 60 * 4:
    cur = req_cur()
    return {'AMD': cur['rates']['AMD'], 'RUB': cur['rates']['RUB'], 'last': time.time()}
  else:
    return cur
    

def build_message(cur, amount, base):
  if base.upper() == 'USD':
    rub_amount = round(cur['RUB'] * amount, 2)
    amd_amount = round(cur['AMD'] * amount, 2)
    
    return f'{amount} USD is {rub_amount} RUB and {amd_amount} AMD'
  elif base.upper() == 'AMD':
    usd_amount = round(amount / cur['AMD'], 2)
    rub_amount = round(cur['RUB'] * usd_amount, 2)
    
    return f'{amount} AMD is {usd_amount} USD and {rub_amount} RUB'
  elif base.upper() == 'RUB':
    usd_amount = round(amount / cur['RUB'], 2)
    amd_amount = round(cur['AMD'] * usd_amount, 2)
    
    return f'{amount} RUB is {usd_amount} USD and {amd_amount} AMD'


API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['rate'])
def hello(message):
  global cur
  split_message = message.text.split(' ')
  amount = int(split_message[1])
  base = split_message[2]
  cur = update_cur()

  msg = build_message(cur, amount, base)
  bot.reply_to(message, msg)


bot.polling()
