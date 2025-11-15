import streamlit as st
import datetime as dt
import requests
from google import genai
import os

st.title("Phase 3: Gemini + API Page")

key = os.getenv("GEMINI_API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "d4d90f7b23574185aa4dc07c0d33676b"

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

state = st.selectbox("Which state do you live in?", states)
style = st.selectbox("style", ["simple", "detailed"])
extra = st.text_input("extra idea")

url = BASE_URL + "?appid=" + API_KEY + "&q=" + state

r = requests.get(url)

if r.status_code == 200 and key:
    data = r.json()
    k = data["main"]["temp"]
    c = round(k - 273.15, 2)
    f = round(c * 1.8 + 32, 2)
    h = data["main"]["humidity"]
    d = data["weather"][0]["description"]
    rise = dt.datetime.fromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    set = dt.datetime.fromtimestamp(data["sys"]["sunset"] + data["timezone"])
    text = "state: " + state + ". temp c: " + str(c) + ". temp f: " + str(f) + ". humidity: " + str(h) + "."
    text = text + " description: " + d + ". sunrise: " + str(rise) + ". sunset: " + str(set) + "."
    if extra:
        text = text + " extra: " + extra + "."
    prompt = "You get simple weather data. " + text + " Write a " + style + " paragraph about the weather and what someone might do today."
    client = genai.Client(api_key=key)
    out = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    st.write(out.text)
elif not key:
    st.write("no gemini api key was found")
else:
    st.write("there was a problem with the api")


