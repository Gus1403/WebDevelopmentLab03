import streamlit as st
import datetime as dt
import requests

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
    state = st.selectbox("Which state do you live in?", states)
with col2:
    unit = st.selectbox("units", ["celsius", "fahrenheit"])
    view = st.selectbox("view", ["now", "next 5 days"])

if view == "now":
    url = BASE_URL + "?appid=" + API_KEY + "&q=" + state
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        k = data["main"]["temp"]
        c = round(k - 273.15, 2)
        f = round(c * 1.8 + 32, 2)
        h = data["main"]["humidity"]
        d = data["weather"][0]["description"]
        rise = dt.datetime.fromtimestamp(data["sys"]["sunrise"] + data["timezone"])
        set = dt.datetime.fromtimestamp(data["sys"]["sunset"] + data["timezone"])
        with box:
            if c > 25:
                st.subheader("The weather is so hot!")
            elif c > 15:
                st.subheader("The weather is just nice!")
            elif c > 0:
                st.subheader("The weather is getting cold!")
            else:
                st.subheader("It's freezing!")
            if unit == "celsius":
                st.write("The temperature right now is", c, "degrees celsius")
            else:
                st.write("The temperature right now is", f, "degrees fahrenheit")
            st.write("The humidity right now is", h)
            st.write("The weather today can be described as", d)
            st.write("The time of sunrise is", rise)
            st.write("The time of sunset is", set)
            st.bar_chart([c, h])
    else:
        with box:
            st.write("there was a problem with the api")
else:
    url2 = FORECAST_URL + "?appid=" + API_KEY + "&q=" + state
    r2 = requests.get(url2)
    if r2.status_code == 200:
        data2 = r2.json()
        days = {}
        for item in data2["list"]:
            date = item["dt_txt"].split(" ")[0]
            k = item["main"]["temp"]
            c = round(k - 273.15, 2)
            if date not in days:
                days[date] = []
            days[date].append(c)
        names = []
        vals = []
        for d in sorted(days.keys())[:5]:
            t_list = days[d]
            s = 0
            for v in t_list:
                s = s + v
            avg = s / len(t_list)
            if unit == "celsius":
                names.append(d)
                vals.append(round(avg, 2))
            else:
                f = avg * 1.8 + 32
                names.append(d)
                vals.append(round(f, 2))
        with box:
            st.subheader("Average temperature for the next 5 days")
            st.write(names)
            st.line_chart(vals)
    else:
        with box:
            st.write("there was a problem with the api")

