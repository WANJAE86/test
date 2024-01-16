import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 전일 종가와 전일 시가를 구하는 함수
def get_yesterday_close(ticker):
    # 일봉 데이터를 가져옵니다.
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    yesterday_close = df.iloc[0]['close']
    
    # 1일 전의 종가를 반환합니다.
    return yesterday_close

def get_yesterday_open(ticker):
    # 일봉 데이터를 가져옵니다.
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    yesterday_open = df.iloc[0]['open']
    
    # 1일 전의 시가를 반환합니다.
    return yesterday_open


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SOL")
        end_time = start_time + datetime.timedelta(minutes=10)
        
        # 전일 종가 조회
        yesterday_close = get_yesterday_close("KRW-SOL")
        yesterday_open = get_yesterday_open("KRW-SOL")

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-SOL", 0.5)
            current_price = get_current_price("KRW-SOL")
            if target_price < current_price and yesterday_open > yesterday_close:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-SOL", krw*0.9995)
                        print("buy")
        else:
            btc = get_balance("SOL")
            if btc > 0.04:
                upbit.sell_market_order("KRW-SOL", btc*0.9995)
                print("sell")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
