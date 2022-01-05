import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NFL Football Stats Explorer (Rushing)")

st.markdown("""
    This app performs simple webscraping of NFL Football player stats.
    * **Data source**: [pro-football-reference.com](https://www.pro-football-reference.com/years/2020/rushing.htm).
""")

st.sidebar.header("User Input Features")

selected_year = st.sidebar.selectbox("Year", list(reversed(range(2000, 2021))))

@st.cache
def load_data(year):
    url = f"https://www.pro-football-reference.com/years/{year}/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index) # Drop repeating headers
    raw = raw.fillna(0) # Fill in missing values with 0
    playerstats = raw.drop(["Rk"], axis=1) # Drop ranking column
    return playerstats

playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

unique_pos = ["QB", "RB", "WR", "TE", "FB"]
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

# Display a histogram of age
fig, axs = plt.subplots(figsize=(10, 5))
axs.set_title("Age Distribution")
axs.hist(sorted(df_selected_team.Age), bins=10)
st.pyplot(fig)