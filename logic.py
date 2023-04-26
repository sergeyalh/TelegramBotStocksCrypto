import yfinance as yf
import requests


def getPrices(bot, message, stocks):
  response = ""
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='4d', interval='5d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 3)
      format_date = row['Date'].strftime('%d/%m')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <15}{columns[1] : ^15}{columns[2] : >15}\n"
  for row in stock_data:
    response += f"{row[0] : <15}{row[1] : ^15}{row[2] : >15}\n"
  response += "\n" + "/start"
  print(response)
  bot.send_message(message.chat.id, response)


def getCryptoPrices(bot, message, cryptoList):
  j = 0
  # Defining Binance API URL
  key = "https://api.binance.com/api/v3/ticker/price?symbol="
  response = ""
  # running loop to print all crypto prices
  for i in cryptoList:
    # completing API for request
    url = key + cryptoList[j]
    data = requests.get(url)
    data = data.json()
    j = j + 1
    response += f"{data['symbol']} price is {data['price']} \n"
  bot.send_message(message.chat.id, response)
