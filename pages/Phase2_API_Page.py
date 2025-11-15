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
    state1 = st.selectbox("first place", states)
with col2:
    state2 = st.selectbox("second place", states)

unit = st.selectbox("units", ["celsius", "fahrenheit"])

curr_url1 = BASE_URL + "?appid=" + API_KEY + "&q=" + state1
curr_url2 = BASE_URL + "?appid=" + API_KEY + "&q=" + state2
curr_r1 = requests.get(curr_url1)
curr_r2 = requests.get(curr_url2)

if curr_r1.status_code == 200 and curr_r2.status_code == 200:
    w1 = curr_r1.json()
    w2 = curr_r2.json()
    k1 = w1["main"]["temp"]
    c1 = round(k1 - 273.15, 2)
    k2 = w2["main"]["temp"]
    c2 = round(k2 - 273.15, 2)
    h1 = w1["main"]["humidity"]
    h2 = w2["main"]["humidity"]
    
    st.subheader("Current Weather Comparison")
    if unit == "celsius":
        t1 = c1
        t2 = c2
        u = "celsius"
    else:
        t1 = round(c1 * 1.8 + 32, 2)
        t2 = round(c2 * 1.8 + 32, 2)
        u = "fahrenheit"
    
    bar_data = {
        state1: [t1, h1],
        state2: [t2, h2]
    }
    st.bar_chart(bar_data)
    st.write("The first bar for each place is the temperature in", u, "and the second bar is the humidity.")
    st.write("The first place is", state1, "and the second place is", state2, ".")

url1 = FORECAST_URL + "?appid=" + API_KEY + "&q=" + state1
url2 = FORECAST_URL + "?appid=" + API_KEY + "&q=" + state2

r1 = requests.get(url1)
r2 = requests.get(url2)

if r1.status_code == 200 and r2.status_code == 200:
    d1 = r1.json()
    d2 = r2.json()
    days1 = {}
    for item in d1["list"]:
        date = item["dt_txt"].split(" ")[0]
        k = item["main"]["temp"]
        c = round(k - 273.15, 2)
        if date not in days1:
            days1[date] = []
        days1[date].append(c)
    days2 = {}
    for item in d2["list"]:
        date = item["dt_txt"].split(" ")[0]
        k = item["main"]["temp"]
        c = round(k - 273.15, 2)
        if date not in days2:
            days2[date] = []
        days2[date].append(c)
    names = []
    vals1 = []
    vals2 = []
    for d in sorted(days1.keys())[:5]:
        if d in days2:
            t1 = days1[d]
            s1 = 0
            for v in t1:
                s1 = s1 + v
            a1 = s1 / len(t1)
            t2 = days2[d]
            s2 = 0
            for v in t2:
                s2 = s2 + v
            a2 = s2 / len(t2)
            if unit == "celsius":
                vals1.append(round(a1, 2))
                vals2.append(round(a2, 2))
            else:
                f1 = a1 * 1.8 + 32
                f2 = a2 * 1.8 + 32
                vals1.append(round(f1, 2))
                vals2.append(round(f2, 2))
            names.append(d)
    with box:
        st.subheader("Average temperature for the next 5 days")
        st.write(names)
        data = {
            state1: vals1,
            state2: vals2
        }
        st.line_chart(data)
        st.write("The first line is for", state1, "and the second line is for", state2, ".")
else:
    with box:
        st.write("there was a problem with the api")

