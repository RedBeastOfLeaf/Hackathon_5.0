import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)


def speak():
    engine.say("Hello, My name is David")
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()


speak()
