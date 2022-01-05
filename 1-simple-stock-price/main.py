import yfinance as yf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simple Stock Price App", page_icon="📈")

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and **volume** of Google!
         
""")

# Define the ticker symbol
tickerSymbol = st.radio("Which company would you like to see?", ['AAPL', 'TSLA', 'GOOGL'])
# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2021-01-04')

st.write("## Closing Price")
st.line_chart(tickerDf.Close)

st.write("## Volume")
st.line_chart(tickerDf.Volume)