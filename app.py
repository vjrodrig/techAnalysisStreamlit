import yfinance as yf
import streamlit as st
import datetime 
import talib 
import ta
import pandas as pd
import requests
yf.pdr_override()

st.write("""
# Technical Analysis Web Application
Shown below are the **Moving Average Crossovers**, **Bollinger Bands**, **MACD's**, **Commodity Channel Indexes**, and **Relative Strength Indexes** of any stock!
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    # ticker = st.sidebar.text_input("Ticker", 'AAPL')
    ticker = st.sidebar.selectbox("Ticker", (
        'AGUAS-A.SN',
        'ANDINA-B.SN',
        'BESALCO.SN',
        'BSANTANDER.SN',
        'BLUMAR.SN',
        'CAMANCHACA.SN',
        'CAP.SN',
        'CENCOSUD.SN',
        'CENCOSHOPP.SN',
        'COPEC.SN',
        'CONCHATORO.SN',
        'CINTAC.SN',
        'ECL.SN',
        'EISA.SN',
        'EMBONOR-B.SN',
        'ENELCHILE.SN',
        'ENELAM.SN',
        'ENTEL.SN',
        'FALABELLA.SN',
        'FORUS.SN',
        'HITES.SN',
        'INDISA.SN',
        'INGEVEC.SN',
        'LAS-CONDES.SN',
        'SALFACORP.SN',
        'SALMOCAM.SN',
        'TRICOT.SN',
        'MALLPLAZA.SN',
        'MANQUEHUE.SN',
        'MASISA.SN',
        'MOLLER.SN',
        'MULTIFOODS.SN',
        'PARAUCO.SN',
        'PAZ.SN',
        'RIPLEY.SN',
        'SECURITY.SN',
        'SOCOVESA.SN',
        'SONDA.SN',
        'SMSAAM.SN',
        'SMU.SN',
        'SQM-B.SN',
        'VAPORES:SN',
        'WATTS.SN',
        'ZOFRI.SN',




        ))

    start_date = st.sidebar.text_input("Start Date", '2020-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    # url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    url = "http://autoc.finance.yahoo.com/autoc?query={}&region=EU&lang=en-GB".format(symbol)

    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data 
data = yf.download(symbol,start,end)

# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['Adj Close'])

# ## SMA and EMA
#Simple Moving Average
data['SMA'] = talib.SMA(data['Adj Close'], timeperiod = 20)

# Exponential Moving Average
data['EMA'] = talib.EMA(data['Adj Close'], timeperiod = 20)

# Plot
st.header(f"Simple Moving Average vs. Exponential Moving Average\n {company_name}")
st.line_chart(data[['Adj Close','SMA','EMA']])

# Bollinger Bands
data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Adj Close'], timeperiod =20)

# Plot
st.header(f"Bollinger Bands\n {company_name}")
st.line_chart(data[['Adj Close','upper_band','middle_band','lower_band']])

# ## MACD (Moving Average Convergence Divergence)
# MACD
data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# Plot
st.header(f"Moving Average Convergence Divergence\n {company_name}")
st.line_chart(data[['macd','macdsignal']])

## CCI (Commodity Channel Index)
# CCI
cci = ta.trend.cci(data['High'], data['Low'], data['Close'], window=31, constant=0.015)

# Plot
st.header(f"Commodity Channel Index\n {company_name}")
st.line_chart(cci)

# ## RSI (Relative Strength Index)
# RSI
data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

# Plot
st.header(f"Relative Strength Index\n {company_name}")
st.line_chart(data['RSI'])

# ## OBV (On Balance Volume)
# OBV
data['OBV'] = talib.OBV(data['Adj Close'], data['Volume'])/10**6

# Plot
st.header(f"On Balance Volume\n {company_name}")
st.line_chart(data['OBV'])

