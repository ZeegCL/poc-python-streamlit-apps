import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
import ssl

st.title("S&P 500 Stock Price App")

st.markdown("""
    This app retrieves the list of S&P 500 companies and their corresponding **stock closing price** (year-to-date).
    
    ***
""")

st.sidebar.header("User Input Features")

@st.cache
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    ssl._create_default_https_context = ssl._create_unverified_context # ignore ssl certificate error
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby("GICS Sector")

sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect("Select Sector", sector_unique, sector_unique)

df_selected_sector = df[df["GICS Sector"].isin(selected_sector)]

st.header("Display companies in selected sector")
st.write("Data dimension: {} rows and {} columns".format(df_selected_sector.shape[0], df_selected_sector.shape[1]))
st.dataframe(df_selected_sector)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f"<a href='data:file/csv;base64,{b64}' download='SP500_companies.csv'>Download CSV file</a>"
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

data = yf.download(
    tickers = list(df_selected_sector[:30].Symbol),
    period = "ytd",
    interval = "1d",
    group_by = "ticker",
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df["Date"] = df.index
    plt.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    plt.plot(df.Date, df.Close, color="skyblue", alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Closing Price", fontweight="bold")
    st.set_option('deprecation.showPyplotGlobalUse', False) # HACK: disable deprecation warning
    
    return st.pyplot()

num_company = st.sidebar.slider("Number of companies to display", min_value=1, max_value=30, value=5)

if st.button("Show plots"):
    st.header("Stock closing price")
    for symbol in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(symbol)