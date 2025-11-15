import streamlit as st
import datetime as dt
import requests
import plotly.express as px
import pandas as pd

st.title("Phase 2: Weather API Page")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "d4d90f7b23574185aa4dc07c0d33676b"

col1, col2 = st.columns(2)

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

box = st.container()

with col1:
    state1 = st.selectbox("first place", states)
with col2:
    unit = st.selectbox("units", ["celsius", "fahrenheit"])

url0 = BASE_URL + "?appid=" + API_KEY + "&q=" + state1
data0 = requests.get(url0).json()
kelvin = data0['main']['temp']
celsius = round(kelvin - 273.15, 2)
fahrenheit = round(celsius * 1.8 + 32, 2)
humidity = data0['main']['humidity']
description = data0['weather'][0]['description']
sunrise = dt.datetime.fromtimestamp(data0['sys']['sunrise'] + data0['timezone'])
sunrisestr = sunrise.strftime("%H:%M")
sunset = dt.datetime.fromtimestamp(data0['sys']['sunset'] + data0['timezone'])
sunsetstr = sunset.strftime("%H:%M")

with box:
    if celsius > 25:
        st.subheader("The weather is so hot!")
        st.image("Images/Hot.png")
    elif celsius > 15:
        st.subheader("The weather is just nice!")
        st.image("Images/Good.png")
    elif celsius > 0:
        st.subheader("The weather is getting cold!")
        st.image("Images/Cold.png")
    else:
        st.subheader("It's freezing!")
        st.image("Images/Freezing.png")
    if unit == "celsius":
        st.write(f"The temperatuer right now is {celsius} decrees celsius")
    else:
        st.write(f"The temperatuer right now is {fahrenheit} degrees fahrenheit")
    st.write(f"The humidity right now is {humidity}")
    st.write(f"The weather today can be described as {description}")
    st.write(f"The time of sunrise is {sunrisestr} local time")
    st.write(f"The time of sunset is {sunsetstr} local time")
    st.markdown("---")
    st.write(f"Now Let's compare {state1}'s temperature with another")
    state2 = st.selectbox("second place", states)

url1 = FORECAST_URL + "?appid=" + API_KEY + "&q=" + state1
url2 = FORECAST_URL + "?appid=" + API_KEY + "&q=" + state2

data1 = requests.get(url1).json()
data2 = requests.get(url2).json()

days1 = {}
for item in data1["list"]:
    date = item["dt_txt"][:10]
    temp = round((item["main"]["temp"]) - 273.15, 2)
    if date not in days1:
        days1[date] = []
    days1[date].append(temp)

days2 = {}
for item in data2["list"]:
    date = item["dt_txt"][:10]
    k = item["main"]["temp"]
    temp = round((item["main"]["temp"]) - 273.15, 2)
    if date not in days2:
        days2[date] = []
    days2[date].append(temp)

names = []
vals1 = []
vals2 = []

for d in sorted(days1.keys())[:5]:
    time1 = days1[d]
    total1 = 0
    for v in time1:
        total1 = total1 + v
    avg1 = total1 / len(time1)

    time2 = days2[d]
    total2 = 0
    for v in time2:
        total2 = total2 + v
    avg2 = total2 / len(time2)

    if unit == "celsius":
        vals1.append(round(avg1, 2))
        vals2.append(round(avg2, 2))
    else:
        faravg1 = avg1 * 1.8 + 32
        faravg2 = avg2 * 1.8 + 32
        vals1.append(round(faravg1, 2))
        vals2.append(round(faravg2, 2))
    names.append(d)

with box:
    st.subheader("Average temperature for the next 5 days")
    
    df = pd.DataFrame({
    	"day": list(range(len(names))),
    	state1: vals1,
    	state2: vals2
	})
    fig = px.line(
    	df,
    	x="day",
    	y=[state1, state2],
    	labels={"day": "Days since 5 days ago", "value": "Temperature", "variable": "States:"},
    )

    st.plotly_chart(fig)
