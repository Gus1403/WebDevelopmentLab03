import streamlit as st
import datetime as dt
import requests
from google import genai
import os

st.title("Phase 4: Gemini Chatbot Page")

key = os.getenv("GEMINI_API_KEY")

if "chat" not in st.session_state:
    st.session_state.chat = []

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
kind = st.selectbox("question type", ["activity", "clothes"])
q = st.chat_input("ask a question")

url = BASE_URL + "?appid=" + API_KEY + "&q=" + state

r = requests.get(url)

info = ""

if r.status_code == 200:
    data = r.json()
    k = data["main"]["temp"]
    c = round(k - 273.15, 2)
    f = round(c * 1.8 + 32, 2)
    h = data["main"]["humidity"]
    d = data["weather"][0]["description"]
    rise = dt.datetime.fromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    set = dt.datetime.fromtimestamp(data["sys"]["sunset"] + data["timezone"])
    info = "state: " + state + ". temp c: " + str(c) + ". temp f: " + str(f) + ". humidity: " + str(h) + "."
    info = info + " description: " + d + ". sunrise: " + str(rise) + ". sunset: " + str(set) + "."

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["text"])

if q and info and key:
    st.session_state.chat.append({"role": "user", "text": q})
    with st.chat_message("user"):
        st.write(q)
    try:
        client = genai.Client(api_key=key)
        base = "You are a weather helper. Use this data: " + info + " The user wants help about " + kind + "."
        h = ""
        for m in st.session_state.chat:
            h = h + m["role"] + ": " + m["text"] + "\n"
        text = base + " Here is the chat so far:\n" + h + " The question is: " + q + "."
        with st.chat_message("assistant"):
            box = st.empty()
            ans = ""
            r2 = client.models.generate_content_stream(model="gemini-2.5-flash", contents=text)
            for part in r2:
                if part.text:
                    ans = ans + part.text
                    box.write(ans)
        st.session_state.chat.append({"role": "assistant", "text": ans})
    except Exception:
        st.write("there was an error. please try again.")
elif q and not key:
    st.write("no gemini api key was found")
elif q and not info:
    st.write("there was a problem with the api")


