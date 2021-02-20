from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia


def home(request):
    return render(request, 'home.html')


def external(request):
    # initiate recognizer
    r = sr.Recognizer()

    # initiate engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)

    def speak(text):
        engine.say(text)
        engine.runAndWait()

    def greet(hour):
        if hour < 12:
            speak("Good morning, my name is David")
        elif hour < 16:
            speak("Good afternoon, my name is David")
        elif hour < 24:
            speak("Good evening, my name is David")

    def listen():
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            print("Recognizing...")
            command = r.recognize_google(audio)
            print(command)
            return command

        except:
            return None

    hour = datetime.datetime.now().hour
    greet(hour)
    speak("How may I help you?")

    while True:
        def onWord(name, location, length):
            print('word', name, location, length)
            if keyboard.is_pressed("esc"):
                engine.stop()

        engine.connect('started-word', onWord)
        command = listen()
        if command != None:
            command.lower()
        else:
            speak("Please say it again")
            continue

        if 'date' in command:
            now = datetime.datetime.now()
            date = now.date()
            date = "Today's date is, " + str(date)
            speak(date)
        elif 'time' in command:
            now = datetime.datetime.now()
            time = now.strftime("%H:%M")
            time = "Current time is, " + time
            speak(time)
        elif 'Wikipedia' in command:
            speak("Searching wikipedia")
            command = command.replace("search on Wikipedia", "")
            result = wikipedia.summary(command, sentences=2)
            result = "According to Wikipedia, " + result
            speak(result)
        elif 'YouTube' in command:
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            speak("Opening YouTube")
            webbrowser.get(chrome_path).open_new_tab("youtube.com")
        elif 'turn off' in command:
            speak("Turning off")
            engine.stop()
            break
        else:
            speak("Didn't recognise as a command")

    return render(request, 'home.html')
