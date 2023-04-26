import yfinance as yf
from replit import db
import os
import requests


def command(bot, message):
  incomeTextArray = message.text.split(" ")
  incomeTextSize = len(incomeTextArray)
  if incomeTextSize != 3:
    if message.text.startswith('Chat: '):
      response = requests.post(
        "https://api.openai.com/v1/completions",
        json={
          "prompt": message.text,
          "model": "text-davinci-003"
        },
        headers={
          "Authorization": f"Bearer {os.getenv('OPEN_AI_KEY')}",
        },
      ).json()
      choices = response['choices']
      oneChoinc = choices[0]
      text = oneChoinc['text']
      print(text)
      bot.reply_to(message, response["choices"][0]["text"])
    else:
      bot.reply_to(
        message,
        "Your message is not in the format dude! \n '(Add/Remove) (Stock/Etf/Crypto) (symbol)' to add ot remove assets to protfolio or 'Chat: ' to chat with ChatGPT"
      )
  else:
    incomeTextAction = incomeTextArray[0]
    incomeTextAssetType = incomeTextArray[1]
    incomeTextAssetSymbol = incomeTextArray[2]
    if incomeTextAction in ['Add', 'Remove']:
      if incomeTextAssetType in ['Stock', 'Etf', 'Crypto']:
        if incomeTextAssetType != 'Crypto':
          # HERE we will check the symbol
          data = yf.download(tickers=incomeTextAssetSymbol)
          if data.empty == False:
            incomeTextAssetTypeDBKey = incomeTextAssetType + "s"
            curAssetListText = " "
            curAssetList = db[incomeTextAssetTypeDBKey]
            if incomeTextAction == 'Add':
              curAssetList.append(incomeTextAssetSymbol)
              db[incomeTextAssetTypeDBKey] = curAssetList
              bot.reply_to(
                message, "This Symbol is added to the list, /" +
                incomeTextAssetTypeDBKey + "  to check the new list")
            else:
              if (incomeTextAssetSymbol in curAssetList):
                curAssetList.remove(incomeTextAssetSymbol)
                db[incomeTextAssetTypeDBKey] = curAssetList
                bot.reply_to(
                  message, "This Symbol is removed from the list, /" +
                  incomeTextAssetTypeDBKey + " to check the new list")
              else:
                bot.reply_to(message, "This Symbol is not in the list")
          else:
            bot.reply_to(message, "Not a valid Symbol Or its delisted")
        else:
          # HERE we will check the crypto symbol
          bot.reply_to(message, "This is crypto Symbol")
      else:
        bot.reply_to(message, "Not a valid Asset type")
    else:
      bot.reply_to(message, "Not a valid Action type")
