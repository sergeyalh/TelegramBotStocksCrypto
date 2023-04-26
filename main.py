import os
import telebot
from replit import db
import logic
import textCommand

db['Cryptos'] = ["BTCUSDT", "DOGEUSDT", "LTCUSDT"]
db['Stocks'] = ['sap', 'meta', 'dis', 'wbd', 't', 'sklz', 'hnst']
db['Etfs'] = [
  'xlre', 'spy', 'arkk', 'arkg', 'ksa', 'ixj', 'vti', 'vnq', 'qcln', 'icln',
  'vxus', 'mchi', 'yolo'
]

keyboard1Page = telebot.types.ReplyKeyboardMarkup()
keyboard1Page.row('/Protfolio', '/AddToWishlist', '/RemoveFromWishlist',
                  '/ChatGPT')

keyboard2Protfolio = telebot.types.ReplyKeyboardMarkup()
keyboard2Protfolio.row('/Stocks', '/Etfs', '/Cryptos', '/Return')

API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start', 'Return'])
def start_message(message):
  bot.send_message(message.chat.id,
                   'Hi what do you want /start',
                   reply_markup=keyboard1Page)


@bot.message_handler(commands=['ChatGPT'])
def protfolio(message):
  bot.send_message(
    message.chat.id,
    'Hi! to chat start with "Chat: XXX" for example "Chat: what is the weather in tel aviv"',
    reply_markup=keyboard1Page)


@bot.message_handler(commands=['Protfolio'])
def protfolio(message):
  bot.send_message(message.chat.id,
                   'Hi what do you want /start',
                   reply_markup=keyboard2Protfolio)


@bot.message_handler(commands=['Stocks'])
def get_stocks(message):
  stocks = db['Stocks']
  logic.getPrices(bot, message, stocks)


@bot.message_handler(commands=['Etfs'])
def get_etfs(message):
  etfs = db['Etfs']
  logic.getPrices(bot, message, etfs)


@bot.message_handler(commands=['Cryptos'])
def get_crypto(message):
  cryptos = db['Cryptos']
  logic.getCryptoPrices(bot, message, cryptos)


@bot.message_handler(commands=['AddToWishlist'])
def add_to_wishlist(message):
  bot.send_message(
    message.chat.id,
    "Please reply with: 'Add (Stock/Etf/Crypto(pers)) (symbol)' for example 'Add stock abnb'"
  )


@bot.message_handler(commands=['RemoveFromWishlist'])
def remove_from_wishlist(message):
  bot.send_message(
    message.chat.id,
    "Please reply with: 'Remove (Stock/Etf/Crypto) (symbol)' for example 'Remove stock abnb'"
  )


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
  textCommand.command(bot, message)


bot.polling()
