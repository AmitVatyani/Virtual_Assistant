import json
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
# import _imaging
from PIL import Image
import time
import lyricsgenius

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # to change male voice to female
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:  # calling speech recognizer to listen to source
            print('listening... (start your command with alexa)')
            listener.pause_threshold = 0.5
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def set_reminder(reminder):
    reminder_time = reminder.split('at ')[1]
    reminder_time = time.strptime(reminder_time, '%I:%M %p')
    reminder_time = time.strftime('%H:%M', reminder_time)
    while True:
        current_time = time.strftime('%H:%M')
        if current_time == reminder_time:
            talk('Reminder: ' + reminder.split('at ')[0])
            break
        time.sleep(60)


def get_weather(city):
    api_key = 'your_openweathermap_api_key'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(complete_url)
    data = response.json()
    if data['cod'] != '404':
        weather = data['weather'][0]['description']
        talk('The weather in ' + city + ' is ' + weather)
    else:
        talk('Sorry, I could not find the weather for ' + city)


def find_song_with_lyrics(lyrics):
    genius = lyricsgenius.Genius("YOUR_ACCESS_TOKEN_HERE")
    song = genius.search_song(lyrics)
    if song:
        return f"Found song: '{song.title}' by {song.artist}"
    else:
        return "Song not found"


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'open' in command:
        website = command.replace('open', '')
        talk('Opening ' + website)
        pywhatkit.search(website)

    elif 'remind me' in command:
        talk('What do you want me to remind you about and at what time?')
        reminder = take_command()
        set_reminder(reminder)

    elif 'weather' in command:
        talk('Which city do you want to check the weather for?')
        city = take_command()
        get_weather(city)

    elif 'lyrics' in command:
        lyrics = command.replace('lyrics', '')
        print(lyrics)
        result = find_song_with_lyrics(lyrics)
        talk(result)
        print(result)

    else:
        talk('Please say the command again.')


while True:
    run_alexa()
