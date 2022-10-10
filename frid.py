from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
import webbrowser
import datetime
import time
import wikipedia
import pyttsx3
import os
import subprocess
import wolframalpha
import smtplib
from ecapture import ecapture as ec
import json
import requests


print('Loading your personal assistant - FRIDAY')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetings():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning")
        print("Good Morning")
    elif hour>=12 and hour<16:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        speak("Good Evening")
        print("Good Evening")

def inputcmd():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio=r.listen(source)

        try:
            print("Recognizing...") 
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            
            #print("Sorry, I don't understand")
            speak("Sorry, I don't understand")
            global text
             
            text.insert(INSERT,"Sorry, I don't understand\n")
            return "None"
        return statement

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('testmailfriday@gmail.com', 'Friday@123')
    server.sendmail('testmailfriday@gmail.com', 'nikhil28350@gmail.com', content)
    server.close()
    

def main():
        global root,text
        speak("Tell me how can I help you now?")
        statement = inputcmd().lower()
        

        if 'wikipedia' in statement:
            speak('Searching Wikipedia')
             
            text.insert(INSERT,"Searching Wikipedia\n")
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=2)
            speak("Wikipedia says")
             
            text.insert(INSERT,"Wikipedia Says\n")
            text.insert(INSERT,results)
            speak(results)

       

        elif 'open google' in statement:
            speak("Opening Google")
             
            text.insert(INSERT,"Opening Google\n")
            webbrowser.open_new_tab("https://www.google.com")
            time.sleep(5)

        elif 'open gmail' in statement:
            speak("Opening Google Mail ")
             
            text.insert(INSERT,"Opening Google Mail\n")
            webbrowser.open_new_tab("gmail.com")
            time.sleep(5)

        elif 'open youtube' in statement:
             
            text.insert(INSERT,"Opening Youtube\n")
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Here it is ")
             
            text.insert(INSERT,"Here it is")
            time.sleep(5)

        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"It's {strTime}")
            text.insert(INSERT,strTime)

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            text.delete(INSERT,tk.END)
            text.insert(INSERT,"Whats the city name\n")
            city_name=inputcmd()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                 
                text.insert(INSERT,(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description)))

            else:
                speak(" City Not Found ")
                 
                text.insert(INSERT,"City Not Found\n")

                
        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by KMNP")
             
            text.insert(INSERT,"I was built by KMNP\n")

        elif 'who are you' in statement or 'what can you do' in statement:
             
            text.insert(INSERT,'I am FRIDAY your persoanl assistant. I am programmed to do minor tasks\n')
            speak('I am FRIDAY your persoanl assistant. I am programmed to do minor tasks like'
                  'opening youtube,google chrome,gmail and predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

            
        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are top news from the Times of India')
             
            text.insert(INSERT,"Here are top news from Times of India\n")

            time.sleep(6)


        elif 'ask' in statement:
            speak('What question do you want to ask?')
             
            text.insert(INSERT,"What question do you want to ask")

            question=inputcmd()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
             
            text.insert(INSERT,answer)


        elif 'search'  in statement or "look for" in statement  :
            statement = statement.replace("search","look for", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

            
        elif "log off" in statement or "sign out" in statement:
            speak("Please close all your applications,your system will shutdown in 10 seconds")
             
            text.insert(INSERT,"Please close all your applications,your system will shutdown in 10 seconds\n")

            subprocess.call(["shutdown", "/l"])

        elif "goodbye" in statement or "ok bye" in statement:
            speak('your personal assistant FRIDAY is shutting down,bye')
             
            text.insert(INSERT,'your personal assistant FRIDAY is shutting down,bye\n')
            root.destroy()


        elif 'email' in statement or "mail" in statement:
            try:
                speak("What should I write?")
                 
                text.insert(INSERT,'What should I write?\n')
            
                content = inputcmd()    
                sendEmail(content)
                speak("Email has been sent!")
                 
                text.insert(INSERT,'Email has been sent\n')
            
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")
                 
                text.insert(INSERT,'Sorry. I am not able to send this email\n')
            


root = Tk()
root.geometry("650x400")
# set min and max size using root.maxsize, root.minsize
root.title("FRIDAY")
bg_frame = Frame(root, bg = "white")

fri = Label(root, text = "FRIDAY : your virtual assistant", bg = "black", fg = "white", cursor = "circle").pack(fill = "x")
#for image: Label(image=file.png) use PIL to take jpg format
img = Image.open("bot.jpeg")
img = img.resize((200,125), Image.ANTIALIAS)

photo = ImageTk.PhotoImage(img)
fri_pic = Label(root, image = photo, borderwidth = 0).pack(side = LEFT, anchor = "center", padx = 30)
mic_img = Image.open("mic1.jpeg")
mic_img = mic_img.resize((30,30), Image.ANTIALIAS)
mic_photo = ImageTk.PhotoImage(mic_img)
mic_btn = Button(root, image = mic_photo, borderwidth = 0, command = lambda : main()  ).pack(side = BOTTOM, anchor = "sw", pady = 20)

text = Text(root, width = 30, height = 10)
text.pack(side = BOTTOM, anchor = "center" )
#pack returns a NoneType obj.. do not pack text widget in place.


root.resizable(width= False, height= False)
root["bg" ] = "white"
root.mainloop()
