'''
Date: 2024-04-29 19:44:52
LastEditors: colvinYan && ykwhrimfaxi@gmail.com 
LastEditTime: 2024-04-29 22:51:08
FilePath: /okx-auto-trade/utils/trade.py
Description: functions about trade
Copyright (c) 2024 All Rights Reserved. 
@EMAIL ykwhrimfaxi@gmail.com
'''

import okx.Account as Account
import okx.Trade as Trade

def chekkResult(result):
    if result['code'] == '0':
        return result
    else:
        raise Exception(result)
def GeAccountAPI(tradeMode, debug, api_key, api_secret_key, passphrase):
    return Account.AccountAPI(
        api_key=api_key, 
        api_secret_key=api_secret_key, 
        passphrase=passphrase, 
        use_server_time=False, 
        debug=debug, 
        flag=tradeMode)

def GeTradeAPI(tradeMode, debug, api_key, api_secret_key, passphrase):
    return Trade.TradeAPI(
        api_key=api_key, 
        api_secret_key=api_secret_key, 
        passphrase=passphrase, 
        use_server_time=False, 
        debug=debug, 
        flag=tradeMode)

# URL_ADDRESS
# instId : BTC-USDT-SWAP
# td

# https://www.okx.com/docs-v5/en/?python#trading-account-rest-api-get-balance
# ccy : BTC, ETH, USDT, etc.
# return ccy's balance
def GetBalance(accountAPI, ccy):
    result = chekkResult(accountAPI.get_account_balance(ccy))
    return float(result['data'][0]['details'][0]['availEq'])

'''
description: 默认市价委托的合约
param {*} tradeAPI
param {*} instId: e.g BTC-USDT
param {*} side: buy(开多) / sell (开空)
param {*} price: 以instId 为 BTC-USDT 为例，开多则对应 USDT 数量，开空则对应 BTC 数量
param {*} tpTriggerPx: 止盈触发价
param {*} tpOrdPx: 止盈委托价
param {*} slTriggerPx: 止损触发价
param {*} slOrdPx: 止损委托价
return {*}
'''
def MakeFutureMarketOrder(tradeAPI,instId, side, price,tpTriggerPx, tpOrdPx, slTriggerPx, slOrdPx):
    return chekkResult(tradeAPI.place_order(instId=instId, 
                         tdMode="isolated", 
                         side=side, ordType="market", sz=price,
                         reduceOnly="false",
                         attachAlgoOrds=[{
                            "tpTriggerPx": tpTriggerPx, # 止盈触发价
                            "tpOrdPx": tpOrdPx, # 止盈委托价
                            "tpOrdKind": "condition",
                            "slTriggerPx": slTriggerPx, # 止损触发价
                            "slOrdPx": slOrdPx, # 止损委托价
                            
                         }])) 

def ClosePositions(tradeAPI, instId):
    return chekkResult(tradeAPI.close_positions(instId=instId, mgnMode="isolated"))