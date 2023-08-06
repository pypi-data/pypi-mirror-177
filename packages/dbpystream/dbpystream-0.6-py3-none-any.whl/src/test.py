
import pandas as pd 

import time as t


from api import get_price,auth,get_all_securities,get_index_weights,get_industry_stocks,get_industry,get_trade_days

def test_get_price():
    start_date = "2022-9-10" # 日期字符串格式
    end_date   = "2023-01-30" # 日期字符串格式
    frequency  = "minute" # daily
    fq         = "pre"#"pre"#"post" # pre:前复权[默认]，None
    #codes = ["IF9999.CCFX","TF9999.CCFX"] #603619.XSHG,ZN2210.
    #codes = ["IF9999.CCFX","TF9999.CCFX","000001.XSHE"] #603619.XSHG,ZN2210.
    codes = "600036.XSHG"

    flds  = ["datetime","close"]
    t0 = t.time()

    df  = get_price(codes,start_date,end_date,frequency,fq) ## data为返回的是pd.dataframe格式的数据；
    df.to_csv(r"C:\Users\songroom\Desktop\df.csv")
    print(f"code : {codes} df shape : {df.shape} ")
    print(f"-------------{fq}--------------------")
    print(f"{df.head()}")
    print(f"{df.tail()}")
    print(f"--------------{fq}-------------------")
    print(f"cost time :{t.time()-t0} seconds!")


def test_get_all_securities():
    _type ="stock"
    _date ="2022-10-11"
    df = get_all_securities(types=[_type], date=_date) 
    print(df.head())

def test_get_index_weights():
    _date ="2011-05-31"
    index_id = "000001.XSHG"
    df = get_index_weights(index_id, _date) 
    print(df.head())

def test_get_industry_stocks():
    _date ="2011-05-31"
    industry_id = "I64"
    df = get_industry_stocks(industry_id, _date) 
    print(df.head())

def test_get_industry():
    _date ="2005-06-01"
    code = "600519.XSHG"
    df = get_industry(code, _date) 
    print(df.head())

def test_get_trade_days():
    start_date ="2021-01-01"
    end_date ="2022-10-01"
    df = get_trade_days(start_date, end_date)
    print(f"get_trade_days : {df}")

if __name__== "__main__" :
    auth() # 第一次调用，需要登陆一下
    test_get_all_securities()
    test_get_index_weights()
    test_get_industry_stocks()
    test_get_trade_days()
    test_get_industry()



