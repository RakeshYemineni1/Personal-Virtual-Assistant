import speech_recognition as sr  # For speech recognition
import pyaudio  # Audio input/output support
import webbrowser  # To open URLs in the browser
import pocketsphinx  # Offline speech recognition (not used here)
import pyttsx3  # Text-to-speech conversion
import pygame  # For playing audio files
import music  # Custom module for handling music playback (assumed)
import requests  # For making HTTP requests (e.g., news API)
from openai import OpenAI  # OpenAI API for AI responses
from gtts import gTTS  # Google Text-to-Speech
import os  # For environment variables and file handling
from pydub import AudioSegment  # Audio processing (not used here)

# Function to convert text to speech using Google TTS
def speak(text):
    tts = gTTS(text)
    tts.save("speech.mp3")
    
    pygame.mixer.init()  # Initialize pygame mixer
    pygame.mixer.music.load("speech.mp3")  # Load generated speech
    pygame.mixer.music.play()  # Play the speech
    
    while pygame.mixer.music.get_busy():  # Wait for completion
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()  # Unload the file
    os.remove("speech.mp3")  # Delete the temporary file

# Alternative text-to-speech function using pyttsx3 (local processing)
def speak_old(text):
    speech = pyttsx3.init()
    speech.say(text)
    speech.runAndWait()

# Function to process user commands using OpenAI API
def ai_Process(command):
    API_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment
    
    if not API_key:
        raise ValueError("API key is missing! Set OPENAI_API_KEY in the environment.")
    
    client = OpenAI(api_key=API_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named saturday skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ],
        max_tokens=50
    )
    return response.choices[0].message.content

# Function to process spoken commands
def processCommand(command):
    try:
        if "open google" in command.lower():
            webbrowser.open_new_tab("https://www.google.co.in")  # Open Google
        elif "open facebook" in command.lower():
            webbrowser.open_new_tab("https://www.facebook.com")  # Open Facebook
        elif "open youtube" in command.lower():
            webbrowser.open_new_tab("https://www.youtube.com")  # Open YouTube
        elif "open github" in command.lower():
            webbrowser.open_new_tab("https://www.github.com")  # Open GitHub
        elif command.lower().startswith("play"):
            song = command.lower().split(" ")[1]  # Extract song name
            link = music.musics.get(song, None)  # Get song link
            if link:
                webbrowser.open(link)  # Open song link
            else:
                speak("Sorry, I couldn't find that song.")
        elif "tell news" in command.lower():
            API_key = os.getenv("NEWS_API_KEY")  # Get news API key
            if not API_key:
                speak("I couldn't access the news service. Please check your API key.")
                return
            
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_key}"  # API endpoint
            r = requests.get(url)
            
            if r.status_code == 200:  # Check API response
                data = r.json()
                articles = data.get('articles', [])
                
                if articles:
                    for article in articles[:5]:  # Read top 5 news headlines
                        speak(article['title'])
                else:
                    speak("I couldn't find any recent news.")
            else:
                speak("Sorry, I'm unable to fetch the news right now.")
        else:
            content = ai_Process(command)  # Process command using AI
            speak(content)  # Respond with AI-generated content
    except Exception as e:
        print(f"Error: {e}")  # Log error
        speak("Sorry, I encountered an error while processing your request.")

# Main function to listen and process voice commands
if __name__ == "__main__":
    while True:
        recognizer = sr.Recognizer()  # Initialize speech recognizer
        print("Recognizing.....")
        
        try:
            with sr.Microphone(device_index=1) as source:  # Use microphone
                print("Listening.....")
                
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Capture audio
                word = recognizer.recognize_google(audio)  # Convert speech to text
                print(word)
                
                if word.lower() == "saturday":  # Wake word
                    speak("Yes!, How May I Assist You.....")
                    print("Yes!, How May I Assist You.....")

                    audio_Command = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Listen for command
                    command = recognizer.recognize_google(audio_Command)  # Convert command to text

                    print(f"The Command: {command}")
                    processCommand(command)  # Process command
                
                if word.lower() == "stop":  # Stop execution
                    speak("Exiting....")
                    print("Exiting....")
                    break
        except sr.RequestError:
            print("API is not Available")  # Speech recognition API error
        except sr.WaitTimeoutError:
            print("No Speech Detected, Please Try Again")  # No input detected
        except sr.UnknownValueError:
            print("Could not understand, Please Try Again")  # Unrecognized speech
