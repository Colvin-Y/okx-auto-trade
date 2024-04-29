'''
Date: 2024-04-29 13:54:34
LastEditors: colvinYan && ykwhrimfaxi@gmail.com 
LastEditTime: 2024-04-29 23:16:59
FilePath: /okx-auto-trade/main.py
Description: https://www.okx.com/docs-v5/en/?python#overview-websocket-subscribe 
Copyright (c) 2024 All Rights Reserved. 
@EMAIL ykwhrimfaxi@gmail.com
'''
import okx.Trade as Trade
from utils import util
from utils.defer import defers
from utils import trade
import threading

# https://www.okx.com/docs-v5/en/#overview-demo-trading-services to apply your own api_key and secret_key
api_key = ''
secret_key = ''
passphrase = ''

RUNNING_TIME_SECONDS = 300 # total running time
REQUEST_INTERVAL_SECONDS = 2.0 # get trade info interval
INST_ID = "BTC-USDT"
TRADE_MODE = "1" # live trading:0 , demo trading：1
LEVER = "8" # 杠杆倍数为 8
DEBUG = False

@defers
def main():
    marketAPI = util.GeMarketAPI(TRADE_MODE,DEBUG, api_key, secret_key, passphrase)
    recordTransInfoThd = threading.Thread(target=util.RunFunctionForDuration, 
                                          args=(util.RecordLasteTradeInfo, 
                                                RUNNING_TIME_SECONDS, REQUEST_INTERVAL_SECONDS, INST_ID, marketAPI))
    # record trans info to local
    recordTransInfoThd.start()
    defer: recordTransInfoThd.join() # type: ignore

    # Api calls example:
    accountAPI = trade.GeAccountAPI(TRADE_MODE, DEBUG, api_key, secret_key, passphrase)
    
    # 设置持仓模式并设置永续合约的杠杆倍率为 LEVER
    accountAPI.set_position_mode(posMode="net_mode")
    accountAPI.set_leverage(instId=INST_ID, lever=LEVER, mgnMode="isolated", posSide="long")

    balance_btc = trade.GetBalance(accountAPI, "BTC") # show balance
    balance_USDT = trade.GetBalance(accountAPI, "USDT")
    print(balance_btc)
    print(balance_USDT)

    tradeAPI = trade.GeTradeAPI(TRADE_MODE, DEBUG, api_key, secret_key, passphrase)
    # tradeAPI.place_order()
    # trade.MakeFutureMarketOrder(tradeAPI, INST_ID, "buy", "100",71000,70000,60000,59000) # 市价开多 成本 100 USDT, 带止盈止损
    # trade.MakeFutureMarketOrder(tradeAPI, INST_ID, "sell", "0.05",60000,59000,71000,70000) # 市价开空 成本 0.05 BTC, 带止盈止损

    # trade.MakeFutureMarketOrder(tradeAPI, INST_ID, "buy", "100") # 合约开多 成本 1USDT
    # trade.MakeFutureMarketOrder(tradeAPI, INST_ID, "sell", "0.001") # 合约开空 成本 0.001 BTC
    # trade.ClosePositions(tradeAPI, INST_ID) # 市价全平, 前提是止盈止损单要撤了，撤单接口还没找到是哪个，先这样吧

main()
# result:
## instId:  BTC-USDT