import yfinance as yf

df=yf.download("MSFT",period='1mo',interval='1d')
# print(df)
from finta import TA

df1=TA.SMA(df,period=10,column="volume")
print(df1)
import requests

