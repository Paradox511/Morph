from datetime import datetime
import speech_recognition as sr
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
#Mở âm thanh
from playsound import playsound
#truy cập, xử lí file hệ thống
import os
#Truy cập web, trình duyệt, hỗ trợ tìm kiếm
from googletrans import Translator
from youtube_search import YoutubeSearch
import wikipedia
import queue
import requests
import subprocess
from googlesearch import search
from PIL import Image,ImageTk


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Queue for communication between threads
response_queue = queue.Queue()

# Function to speak given text
def speak(text,language='en'):
    if language == 'vi':
        engine.setProperty('voice', 'Vietnamese')  # Set the voice to Vietnamese
    else:
        engine.setProperty('voice', 'english')  # Set the voice to English
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
    pass

# Function to handle text input
def handle_text_input(event=None):
    query = entry.get()
    handle_input(query)


def check_weather(location):
    api_key = "d87af97fceea94d4f615de0195a5e26a"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = {
                "description": weather_description,
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed
            }

            return weather_info
        else:
            print(f"Failed to retrieve weather data: {data['message']}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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

def open_application(application_name):
    try:
        subprocess.Popen([application_name])  # Replace with the actual application name or path
    except FileNotFoundError:
        print("Application not found.")

def get_news_headlines():
    news_api_key = "de6633428bf142d0bc51918f7eb5da78"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles'][:3]]
        return headlines
    except Exception as e:
        print("Error fetching news:", e)
        return []

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "Too many results. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        return "No information found. Please try again."


def play_music(song_name):
    # Replace with your music directory
    music_directory = "C:/Users/ADMIN/Desktop/Python/MorphAI/music"
    song_path = os.path.join(music_directory, song_name)

    if os.path.exists(song_path):
        os.system(f"start {song_path}")  # On Windows
        # For Linux or MacOS, you can use something like:
        # os.system(f"xdg-open {song_path}")
    else:
        print("Song not found.")

def func():
    text = """
        Supported functions:
        1.Greeting
        2.Date, Time
        3.Check weather
        4.Google search
        5.Youtube search
        6.play local music
        7.Wikipedia search
        8.Translate text (eng <--> vi)
        9.Check news headlines
        10.Open application
        11.Exit
    """
    speak(text)
    return text
def translate_text(text):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest='vi')
        return translated_text.text
    except Exception as e:
        print("Translation error:", e)
        return "Sorry, translation failed."

# Function to handle both speech and text input
# Function to handle both speech and text input
# Function to handle both speech and text input
def handle_input(query):
    global search_results

    if "hello" in query.lower():
        response_text = "Hello! How can I assist you?"
        speak(response_text)
    elif "function" in query.lower():
        response_text = func()
    elif "time" in query.lower():
        current_time = datetime.now().strftime("%I:%M %p")  # Get current time
        response_text = f"The current time is {current_time}."
        speak(response_text)
    elif "date" in query.lower():
        today = datetime.today().strftime("%A, %m/%d/%Y")
        response_text = f"Today is {today}"
        speak(response_text)
    elif "weather" in query.lower():
        location = query.lower().replace("weather", "").strip()
        weather_info = check_weather(location)
        if weather_info:
            response_text = f"Weather Information in {location}:\n"+f"Description: {weather_info['description']}\n"+f"Temperature: {weather_info['temperature']}°C\n"+f"Humidity: {weather_info['humidity']}%\n"+f"Wind Speed: {weather_info['wind_speed']} m/s"
            speak(response_text)
        else:
            response_text = "Failed to retrieve weather information."
            speak(response_text)
    elif "google" in query.lower():
        search_query = query.lower().replace("google", "").strip()
        url = f"google.com/search?q={search_query}"
        wb.open(url)
        response_text = f"Here are your results on {search_query}"
    elif "open" in query.lower():
        application = query.lower().replace("open","").strip()
        response_text = f"Opening {application}"
        open_application(application)
    elif "play music" in query.lower():
        song = query.lower().replace("play music","").strip()
        response_text = f"Now playing {song}"
        play_music(song)
    elif "news" in query.lower():
        headlines = get_news_headlines()
        response_text = f"Here are the latest news headlines:\n"
        for i,headline in enumerate(headlines):
            response_text += f"{i+1}. {headline}\n"
        speak(response_text)
    elif "wikipedia" in query.lower() or "wiki" in query.lower():
        search_query = query.lower().replace("wikipedia", "").strip()
        response_text = search_wikipedia(search_query)
        speak(response_text)
    elif "translate" in query.lower():
        text_to_translate = query.lower().replace("translate", "").strip()
        translated = translate_text(text_to_translate)
        speak(translated, language='vi')
        response_text = translated
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
            response_text = f"Opening: {selected_video['title']}"
            speak(response_text)
            speak("Enjoy your video!")
            # Open the selected video URL
            wb.open(selected_video['url'])
            search_results=None
            return  # Exit function after opening the video
        else:
            response_text = "Invalid selection. Please choose a number within the range."
    elif "exit" in query.lower():
        response_text = "Goodbye!"
        root.destroy()
    else:
        response_text = "Sorry, I couldn't understand your request."

    response_text = response_text.strip()
    text_box.insert(tk.END, response_text + "\n")
    response_queue.put(response_text)

    text_box.yview_moveto(1.0)
    entry.delete(0, tk.END)
    pass



def speak_search_results(search_results):
    for i, result in enumerate(search_results):
        speak(f"{i+1}. {result['title']}")
        time.sleep(2)  # Adjust the delay between speaking each result





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
root.geometry("600x400")

# Create frames
input_frame = ttk.Frame(root)
output_frame = ttk.Frame(root)
input_frame.pack(pady=10)
output_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

# Text entry
entry = ttk.Entry(input_frame, width=50)
entry.grid(row=0, column=0, padx=5, pady=5)
entry.bind("<Return>", handle_text_input)

# Text button
text_button = ttk.Button(input_frame, text="Submit", command=handle_text_input)
text_button.grid(row=0, column=1, padx=5, pady=5)

# Speech button with icon
speech_icon = Image.open("Microphone.png")
speech_icon = speech_icon.resize((24, 24))
speech_icon = ImageTk.PhotoImage(speech_icon)
speech_button = ttk.Button(input_frame, image=speech_icon, command=handle_speech_input)
speech_button.grid(row=0, column=2, padx=5, pady=5)

# Text box to display AI's responses
text_box = tk.Text(output_frame, height=10, width=50)
text_box.pack(fill=tk.BOTH, expand=True)

# Run the GUI
root.mainloop()
