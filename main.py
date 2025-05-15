"""
Project: Jarvis Voice Assistant
Module: musicLibrary.py
Description: Stores a dictionary mapping song names to their respective YouTube links.
This module helps Jarvis play music via voice commands.

Author: Hashir Adnan
GitHub: https://github.com/thfnexus  
Date: 2025-05-14
"""


import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"  # Make sure to replace this with your News API key

# Function for speaking old method using pyttsx3
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Function for speaking with gTTS (Google Text-to-Speech)
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')  # Save speech as a temporary MP3 file

    # Initialize Pygame mixer to play MP3
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    # Keep the program running until music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")  # Clean up temporary file

# Function for processing AI requests using OpenAI GPT-3
def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>")  # Replace with your OpenAI API key

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

# Function to handle user commands
def processCommand(c):
    c = c.lower()  # Convert command to lowercase for case-insensitivity

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]  # Extract the song name
        link = musiclibrary.music.get(song)  # Look up the song link in the music library
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c:
        fetch_news()
    else:
        # Let OpenAI handle the command
        output = aiProcess(c)
        speak(output)

# Function to fetch top news articles
def fetch_news():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])

        # Read out the headlines
        if articles:
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, no news found.")
    else:
        speak("Sorry, I couldn't fetch the news right now.")

# Main loop for activating Jarvis with a wake word
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    
    while True:
        r = sr.Recognizer()
        print("Listening for 'Jarvis'...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes, how can I assist you?")
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for your command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)  # Process the command
        except Exception as e:
            print(f"Error: {e}")
