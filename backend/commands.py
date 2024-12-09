import os
import eel
from playsound import playsound
import time
import random
import webbrowser
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
from bs4 import BeautifulSoup
import pywhatkit
import smtplib
import sys
from tkinter.filedialog import askopenfilename
import PyPDF2
import psutil
import cv2
import pyautogui
import pyjokes
import requests
import speedtest
from instaloader import instaloader
# import ai21
import openai
from backend.Face_recognition import recognize_face
from backend.Emotion_detection import main


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    eel.DisplayMessage(audio)
    engine.runAndWait()

# def playAssistantSound():
#     music_dir = r"D:\Ad_Voice_assistant\frontend\assests\audio\start_sound.mp3"
#     playsound(music_dir)

def take_command():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        eel.DisplayMessage('recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)

    except Exception as e:
        speak("Please repeat, I was unable to understand")
        return "None"
    
    return query

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("How may I help you?")


def pdf_reader():
    book = askopenfilename()
    pdf_reader = PyPDF2.PdfFileReader(book)
    pages = pdf_reader.numPages
    speak(f"Total number of pages in this book: {pages}")
    speak("Please enter the page number I have to read")
    pg = int(input("Please enter the page number: "))
    page = pdf_reader.getPage(pg)
    text = page.extractText()
    speak(text)


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("your_email@gmail.com", "your_password")
    server.sendmail("your_email@gmail.com", to, content)
    server.close()


def scrape_news():
    url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.findAll('h3', attrs={'class': 'ipQwMb ekueJc RD0gLb'})
    for n in news:
        print(n.text)
        speak(n.text)
    print('For more information visit: ', url)
    speak('For more information visit Google news')


def web_scrape(topic):
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = '\n'.join([p.get_text() for p in paragraphs])

# def detect_faces(image):
#     face_locations = face_recognition.face_locations(image)
#     return face_locations

# def capture_video():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         face_locations = detect_faces(frame)

#         for top, right, bottom, left in face_locations:
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

#         cv2.imshow('Face Recognition', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

def adjust_volume(action):
    if action == "up":
        pyautogui.press("volumeup")
    elif action == "down":
        pyautogui.press("volumedown")
    elif action == "mute":
        pyautogui.press("volumemute")


def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")


def _abs(a):
    pass


def abs(a):
    "same as abs(a)."
    return _abs(a)


def add(a, b):
    "same as a + b."
    return a + b


def and_(a, b):
    "same as a & b."
    return a & b


def floondiv(a, b):
    "same as a // b."
    return a // b


def index(a):
    "same as a.__index__()>"
    return a.__index__()


def inv(a):
    "same as ~a."
    return ~a


invert = inv


def ishift(a, b):
    "same as a << b."
    return a << b


def mod(a, b):
    "same as a % b."
    return a % b


def mul(a, b):
    "same as a * b."
    return a * b


def open_application(app_name):
    if app_name.lower() == "chrome":
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif app_name.lower() == "notepad":
        os.startfile("C:\\Windows\\System32\\notepad.exe")


def close_application(app_name):
    os.system(f"taskkill /f /im {app_name}.exe")


def switch_window():
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.keyUp("alt")


def system_command(command):
    if "shutdown" in command:
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        os.system("shutdown /r /t 5")
    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def interact_with_openai():
    speak("You can start interacting with the AI. Speak 'exit' to stop.")
    while True:
        user_input = take_command().lower()
        if user_input == 'exit':
            speak("Exiting AI interaction.")
            break

        # Send user input to the AI model
        response = openai.Completion.create(
            model="babbage-002",  # Choose the model you want to use
            prompt=user_input,
            temperature=0.7,  # Adjust temperature to control creativity
            max_tokens=100  # Adjust max tokens based on desired response length
        )

        # Get AI response and speak it
        ai_response = response.choices[0].text.strip()
        speak("AI says: " + ai_response)


def listen_for_wake_up():
    while True:
        query = take_command().lower()
        global isawake
        if "wake up" in query:
            isawake = True
            return True  # Wake-up statement detected
        elif "rest" in query or "sleep" in query:
            speak("Going to sleep. Say 'wake up' to activate me.")
            return False
        while True:
            query = take_command().lower()
            if "wake up" in query:
                return True  # Wake-up statement detected


# def listen_for_wake_up():
#     while True:
#         query = take_command().lower()
#         if "wake up" in query:
#             return True  # Wake-up statement detected
#         elif "rest" in query or "sleep" in query:
#             speak("Going to sleep. Say 'wake up' to activate me.")
#             return False
#


def start_assistant():
    speak("Assistant is ready.")
    speak("Sifra this side")
    greet()
    if listen_for_wake_up() :
        recognize_face()

        speak("Face recognized.")
        speak("How may I assist you?")
        
        while True:
            
            isawake = True
            if isawake:
                query = take_command().lower()

            else:
                query = ""
                listen_for_wake_up()


            if "read pdf" in query:
                pdf_reader()

            elif "detect my emotion" in query:
                speak("Starting emotion detection...")
                main()



            elif "how are you" in query:
                speak("I am good what's about you sir.")

            elif "i am good" in query:
                speak("nice, sir how me i help you")

            elif "who are you" in query:
                speak("i am Sifra your personal assistant,sir")

            elif "who made you" in query:
                speak("I was made by my friends.")

            elif "thank you" in query or "thanks" in query:
                speak("it's my pleasure sir,")



            elif "open command prompt" and "open cmd" in query:
                os.system("start cmd")

            elif "tell time" in query:
                tell_time()


            elif "ip address" in query:
                ip = requests.get('https://api.ipify.org').text
                speak(f'your ip address is {ip}')


            elif "wikipedia" in query:
                speak("searching wikipedia")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)

            elif "instagram" in query:
                webbrowser.open("www.instagram.com")



            elif "send email" in query:
                try:
                    speak("What should I say?")
                    content = take_command().lower()
                    to = "recipient_email@gmail.com"
                    send_email(to, content)
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("Sorry, unable to send email")

            elif "search on google" in query:
                speak("What do you want to search for?")
                search_query = take_command().lower()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

            elif "search on youtube" in query:
                speak("What do you want to search for on YouTube?")
                search_query = take_command().lower()
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

            elif "play music" in query:
                music_dir = "C:\\Path\\to\\your\\music\\folder"
                songs = os.listdir(music_dir)
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))

            elif 'type' in query:  # 10
                query = query.replace("type", "")
                pyautogui.write(f"{query}")

            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "today's news" in query:
                scrape_news()

            elif "take screenshot" in query or "take a screenshot" in query:
                speak("sir, please tell me the name for this screenshot file")
                name = take_command().lower()
                speak("please sir hold for a seconds, i am taking screenshot")
                time.sleep(2)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak(
                    "i am done sir,the screenshot has been saved, now i am ready for next task")


            elif "instagram profile" in query:
                speak("sir please enter the user name correctly.")
                name = input("enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"sir here is the profile of the user {name}")
                time.sleep(5)
                speak("sir would you like to download profile picture of this account.")
                condition = take_command().lower()
                if "yes" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak(
                        "i am done sir,profile picture is saved in our main folder. now i am ready")
                else:
                    pass


            elif "where i am now" in query or "my location" in query:
                speak("wait sir, let me check our location")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    # print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(
                        f"sir i am not sure, but i think we are in {city} city of {country} country")
                except Exception as e:
                    speak(
                        "sorry sir,due to network issue i am not able to find where we are.")
                    pass



            elif "read pdf" in query:
                pdf_reader()

            elif "today's weather" in query:
                search = "temperature in Mumbai"
                url = f"https;//www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak("current {search} is {temp}")



            elif "how much power left" in query or "how much power we have" in query or "battery" in query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"sir our system have {percentage} percent battery")
                if percentage >= 75:
                    speak("we have enough power to continue our work")
                elif percentage >= 40 and percentage <= 75:
                    speak(
                        "we should connect our system to charging point to charge our battery")
                elif percentage <= 15 and percentage <= 30:
                    speak(
                        "we don't have enough power to work, please connect to charging")
                elif percentage <= 15:
                    speak(
                        "we have very low power, please connect to charging the system will shutdown very soon")



            elif "internet speed" in query or "network speed" in query:
                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(
                    f"sir we have{dl} bit per second downloading speed and {up} bit per second uploading speed")





            elif "volume" in query:
                if "up" in query:
                    adjust_volume("up")
                elif "down" in query:
                    adjust_volume("down")
                elif "mute" in query:
                    adjust_volume("mute")

            elif "open" in query:
                app_name = query.split("open ")[-1]
                open_application(app_name)

            elif "close" in query:
                app_name = query.split("close ")[-1]
                close_application(app_name)

            elif "switch window" in query:
                switch_window()

            elif "shutdown the system" in query or "restart the system" in query or "sleep the system" in query:
                system_command(query)

            # elif "enter ai mode" in query:
            #     interact_with_openai()

            elif "exit" in query:
                speak("Goodbye!")
                sys.exit()

            elif "rest" in query or "sleep" in query:
                speak("Going to sleep. Say 'wake up' to activate me.")
                isawake = False


            # else:
            #    speak("Going to sleep. Say 'wake up' to activate me.")
    
@eel.expose
def main():
    # playAssistantSound()
    start_assistant()

