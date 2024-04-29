'''
Date: 2024-04-29 17:01:19
LastEditors: colvinYan && ykwhrimfaxi@gmail.com 
LastEditTime: 2024-04-29 23:16:19
FilePath: /okx-auto-trade/utils/util.py
Description: 
Copyright (c) 2024 All Rights Reserved. 
@EMAIL ykwhrimfaxi@gmail.com
'''
import json
import okx.MarketData as MarketData
import time
import csv
import datetime
import pytz

BATCH_WRITH_SIZE = 5 # max datas in memory, when reached, write it to csv file
MAX_CSV_DATA_FILE_SIZE = 10 # each csv file max rows

def ParseToJson(jsonDataStr):
    return json.loads(jsonDataStr)

class Trade:
    def __init__(self, timestamp, price):
        self.timestamp = timestamp
        self.price = price
Trades = []

def AppendToCsv(file, rows):
    writer = csv.writer(file)
    writer.writerows(rows)

def CountCsvRows(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for _ in reader)
        return row_count
    except FileNotFoundError:
        return 0

def GetFileName(instId):
    fileNumber = 0
    while True:
        fileName = './data/'+instId+str(fileNumber)+'.csv'
        rows = CountCsvRows(fileName)
        if rows > MAX_CSV_DATA_FILE_SIZE:
            fileNumber += 1
        else:
            return fileName
        
def timestampMillSecondToRfc(timestampMilliseconds):
    dt = datetime.datetime.fromtimestamp(timestampMilliseconds / 1000.0)
    rfcDatetime = dt.astimezone(pytz.timezone('Asia/Shanghai')).isoformat()

    return rfcDatetime

def RecordTrades(timestamp, prices, instId):
    trade = Trade(timestamp, prices)
    Trades.append(trade)

    # do not consider thread safe one, this is a signle-thread-model now
    # batch write so save io overhead
    if len(Trades)>BATCH_WRITH_SIZE:
        fileName = GetFileName(instId)
        
        with open(fileName, 'a', newline='') as f:
            rows = [[timestampMillSecondToRfc(t.timestamp),t.timestamp, t.price] for t in Trades]
            AppendToCsv(f, rows)
        Trades.clear()

def GeMarketAPI(tradeMode, debug,api_key, api_secret_key, passphrase):
    return MarketData.MarketAPI(flag = tradeMode, debug=debug, api_key=api_key,api_secret_key=api_secret_key, passphrase=passphrase)


'''
description: record lastest trade info to local file
param {*} instId:
    BTC-USDT: BTC-USDT SPOT(币币)
    BTC-USDT-MARGIN: BTC-USDT MARGIN(杠杆)
    BTC-USDT-SWAP: BTC-USDT SWAP(永续)
    BTC-USDT-OPTION: BTC-USDT OPTION(期权)
    BTC-USDT-FUTURES: BTC-USDT FUTURES(交割合约)
    BTC-USDT-ANY: BTC-USDT ANY(全部)
param {*} falg: live trading: 0, demo trading: 1
return {*}

API-get_ticker return params: https://www.okx.com/docs-v5/en/?python#order-book-trading-market-data-get-ticker
'''
def RecordLasteTradeInfo(instId, marketDataAPI):
    result = marketDataAPI.get_ticker(instId = instId)
    # only record last traded price, last traded size and timestamp
    if result['code'] == '0':
        lastTradedPrice = float(result['data'][0]['last'])
        timestampMillisec = int(result['data'][0]['ts'])
        RecordTrades(timestampMillisec, lastTradedPrice, instId)


def RunFunctionForDuration(func, durationSec, intervalSec, *args, **kwargs):
    startTime = time.time()
    endTime = startTime + durationSec
    
    while time.time() < endTime:
        func(*args, **kwargs)
        time.sleep(intervalSec)
    