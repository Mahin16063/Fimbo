import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak a given text
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()