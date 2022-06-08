import random

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyowm
import webbrowser
from weatherapi import OPENWEATHER


listener = sr.Recognizer()
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
alexa.setProperty('voice', voices[0])


def speake(text):
    alexa.say(text)
    alexa.runAndWait()


def reach_command():
    try:
        with sr.Microphone() as source:
            print('alexa is waiting for command ......')
            voice = listener.listen(source)
            listener_com = listener.recognize_google(voice)
            command = listener_com.lower()
            if 'alexa' in command:
                print(command)

    except sr.WaitTimeoutError:
        pass
    except sr.UnknownValueError:
        pass
    return command


def get_weather(self, command):
    home = 'chemnitz City, germany'
    owm = pyowm.OWM(OPENWEATHER)
    mgr = owm.weather_manager()

    if "now" in command:
        observation = mgr.weather_at_place(home)
        w = observation.weather
        temp = w.temperature('Celsius')
        status = w.detailed_status
        speake("It is currently " + str(int(temp['temp'])) + " degrees and " + status)
    else:
        print("I haven't programmed that yet.")


def run_alexa():
    try:
        global command
        command = reach_command()
        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            speake('Current time is ' + time)

        elif 'play' in command:
            song = command.replace('play', '')
            speake('playing ' + song)
            pywhatkit.playonyt(song)

        elif 'tell me about' in command:
            search = command.replace('tell me about', '')
            data = wikipedia.summary(search, 1)
            print(data)
            speake(data)
        elif "how are you" in command:
            feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]

            greeting = random.choice(feelings)
            print(greeting)
            speake(greeting)

        elif 'open facebook'in command:
            webbrowser.open('https://www.facebook.com')

        elif "open weather now" in command:
            get_weather(command)
            pass

        elif 'joke' in command:
            speake(pyjokes.get_joke())

        elif 'wish me today my birthday' in command:
            speake('oh, sorry happy birthday to you')

    except TypeError:
        print("Warning: You're getting a TypeError somewhere.")
        pass
    except AttributeError:
        print("Warning: You're getting an Attribute Error somewhere.")
        pass
    except:
        speake('I did not get it but I am going to search it for you')
        pywhatkit.search(command)


while True:
    run_alexa()
