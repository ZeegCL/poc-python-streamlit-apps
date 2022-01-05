from pandas.core.algorithms import unique
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Player Stats Explorer")

st.markdown("""
This app performs exploratory data analysis on NBA player statistics.
* **Data source**: [basketball-reference.com](https://www.basketball-reference.com)
""")

st.sidebar.header("User Input Features")

selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2022))))

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(["Rk"], axis=1)
    
    return playerstats

playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

unique_pos = ["PG", "SG", "SF", "PF", "C"]
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

df_selected_team = playerstats[playerstats.Tm.isin(selected_team) & playerstats.Pos.isin(selected_pos)]

st.header("Display Player Stats of Selected Team(s)")
st.write("Data Dimension: {} rows and {} columns".format(df_selected_team.shape[0], df_selected_team.shape[1]))
st.dataframe(df_selected_team.astype(str))

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f"<a href='data:file/csv;base64,{b64}' download='NBA_Player_Stats_{selected_year}.csv'>Download CSV file</a>"
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv("temp/output.csv", index=False)
    df = pd.read_csv("temp/output.csv")
    
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(11, 9))
        ax = sns.heatmap(corr, mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
        st.pyplot(f)