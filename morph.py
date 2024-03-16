from datetime import datetime
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk
from re import search
import webbrowser as wb
#Chuyển văn bản thành âm thanh
from gtts import gTTS
import pyttsx3
#Xử lí thởi gian
import time
from datetime import date, datetime
#Lấy thông tin từ web
import requests
import ctypes
import json
import urllib
import urllib.request as urllib2
#Mở âm thanh
from playsound import playsound
#truy cập, xử lí file hệ thống
import os
#Thư viện Tkinter hỗ trợ giao diện
from tkinter.ttk import Frame, Button, Style
from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as mbox
#Truy cập web, trình duyệt, hỗ trợ tìm kiếm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from youtube_search import YoutubeSearch
#from youtubesearchpython import SearchVideos
import wikipedia
#Chọn ngẫu nhiên
import random
#chuyển chữ số sang số
from word2number import w2n #tiếng anh
from vietnam_number import w2n # tiếng việt
import queue
import threading
import requests


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Queue for communication between threads
response_queue = queue.Queue()

# Function to speak given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle speech input
def handle_speech_input():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        handle_input(query)
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn't understand you.")

# Function to handle text input
def handle_text_input(event=None):
    query = entry.get()
    handle_input(query)


def check_weather(location):
    api_key = "pm4fIqzuGb2we74pgxjbG9cpgsXi0eT4"
    url = f"https://api.tomorrow.io/v4/timelines?location={location}&fields=temperature,weatherCode,precipitationProbability,windSpeed&units=metric&timesteps=current&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            current_data = data["data"]["timelines"][0]["intervals"][0]["values"]
            temperature = current_data["temperature"]
            weather_code = current_data["weatherCode"]
            precipitation_probability = current_data["precipitationProbability"]
            wind_speed = current_data["windSpeed"]

            # Convert weather code to description (you can create a mapping based on Tomorrow.io's documentation)
            weather_description = "Weather description based on weather code"

            weather_info = f"Weather in {location.capitalize()}:\nDescription: {weather_description}\nTemperature: {temperature}°C\nPrecipitation Probability: {precipitation_probability}%\nWind Speed: {wind_speed} m/s"
        else:
            weather_info = "Sorry, I couldn't fetch the weather information at the moment."

    except Exception as e:
        weather_info = f"An error occurred while fetching weather information: {str(e)}"

    return weather_info


def search_youtube(query, max_results=5):
    try:
        results = YoutubeSearch(query, max_results=max_results).to_dict()
        videos = []
        for video in results:
            title = video['title']
            url = f"https://www.youtube.com/watch?v={video['id']}"
            videos.append({'title': title, 'url': url})
        return videos
    except Exception as e:
        print("Error occurred during YouTube search:", e)
        return None



# Function to handle both speech and text input
# Function to handle both speech and text input
# Function to handle both speech and text input
def handle_input(query):
    global search_results

    if "hello" in query.lower():
        response_text = "Hello! How can I assist you?"
    elif "time" in query.lower():
        current_time = datetime.now().strftime("%I:%M %p")  # Get current time
        response_text = f"The current time is {current_time}."
    elif "date" in query.lower():
        today = datetime.today().strftime("%A, %m/%d/%Y")
        response_text= f"Today is {today}"
    elif "weather" in query.lower():
        location = query.lower().replace("weather", "").strip()
        weather_info = check_weather(location)
        response_text = weather_info
    elif "youtube" in query.lower():
        search_query = query.lower().replace("youtube", "").strip()
        search_results = search_youtube(search_query)
        if search_results:
            response_text = "Here are some YouTube videos related to your search:\n"
            for i, result in enumerate(search_results):
                response_text += f"{i+1}. {result['title']}\n"
        else:
            response_text = "Sorry, I couldn't find any YouTube videos related to your search."
    elif search_results and query.isdigit():
        selected_index = int(query) - 1
        if 0 <= selected_index < len(search_results):
            selected_video = search_results[selected_index]
            response_text = f"Opening video: {selected_video['title']}"
            speak(response_text)
            speak("Enjoy your video!")
            # Open the selected video URL
            wb.open(selected_video['url'])
            return  # Exit function after opening the video
        else:
            response_text = "Invalid selection. Please choose a number within the range."
    elif "exit" in query.lower():
        response_text = "Goodbye!"
        root.destroy()
    else:
        response_text = "Sorry, I couldn't understand your request."

    # Remove trailing newline characters before inserting text into text box
    response_text = response_text.strip()

    # Insert response text into text box
    text_box.insert(tk.END, response_text + "\n")  # Update text box with response immediately
    response_queue.put(response_text)

    entry.delete(0, tk.END)  # Clear the entry after processing the input






# Function to continuously speak bot responses
def speak_responses():
    while True:
        response_text = response_queue.get()
        speak(response_text)
        #text_box.insert(tk.END, response_text + "\n")
        text_box.see(tk.END)  # Scroll to the bottom of the text box

# GUI setup
root = tk.Tk()
root.title("MorphAI")

# Speech button
speech_button = ttk.Button(root, text="Speech Input", command=handle_speech_input)
speech_button.pack(pady=10)

# Text entry
entry = ttk.Entry(root, width=50)
entry.pack(pady=5)
entry.bind("<Return>",handle_text_input)

# Text button
text_button = ttk.Button(root, text="Text Input", command=handle_text_input)
text_button.pack(pady=5)

# Text box to display AI's responses
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=10)

# Start the thread for speaking responses
response_thread = threading.Thread(target=speak_responses)
response_thread.daemon = True  # Make the thread a daemon so it exits when the main program exits
response_thread.start()

# Run the GUI application
root.mainloop()
