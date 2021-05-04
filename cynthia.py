import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import json
from bs4 import BeautifulSoup
import socket
from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random
import platform

frmsndr = ''
frmpass = ''
socket.getaddrinfo('localhost', 8080)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

user_dct = dict()

prev_users = open('users.txt', 'r')
try:
    for line in prev_users:
        prev_lst = line.strip().split()
        user_dct[prev_lst[0]] = int(prev_lst[1])
except:
    pass
prev_users.close()

user_dct[platform.node()] = user_dct.get(platform.node(), 0) + 1

new_users = open('users.txt', 'w')
for k, v in user_dct.items():
    print(k, v, file=new_users)
new_users.close()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 4 <= hour < 12:
        speak('Good Morning!')
    elif 12 <= hour < 18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak('Hi! I am Cynthia. Please Confirm your credentials.')


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('\nListening...')
        r.pause_threshold = 0.9
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')

    except Exception as e:
        print(e)
        print('Say that again please...')
        speak('Say that again please...')
        return "None"
    return query


def sendemail():
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = frmsndr

    # storing the receivers email address
    msg['To'] = es1.get()

    # storing the subject
    msg['Subject'] = es2.get()

    body = es4.get('1.0', END)

    if es3.get() != '':
        # adding attachment
        attachment = open(es3.get(), "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload(attachment.read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % es3.get())

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(frmsndr, frmpass)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(frmsndr, es1.get(), text)

    # terminating the session
    s.quit()

    speak('Email sent to ' + es1.get())
    print('Email sent to ', es1.get())

    for widgets in root2.winfo_children():
        widgets.destroy()
    root2.destroy()


wishme()


def say():
    query = takecommand().lower()

    if 'who are you' in query:
        print('I am Cynthia and I am at your service. I am created for SBL Mini Project.')
        speak('I am Cynthia and I am at your service. I am created for S B L Mini Project.')

    elif 'why are you' in query:
        print('Unfortunately some students created me :_(')
        speak('Unfortunately some students crated me')

    elif 'news' in query:
        try:
            response = requests.get('https://newsapi.org/v2/top-headlines?'
                                    'country=in&apikey=06b1d7e0b2ed460ebf65aef11999cab6')
            news = json.loads(response.text)
            ctr = 0
            for new in news['articles']:
                print(str(new['title']))
                print(str(new['description']), "\n")
                speak(str(new['title']))
                ctr += 1
                if ctr == 3:
                    break
        except:
            speak("can't access link, plz check you internet ")

    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace('wikipedia', '')
        results = wikipedia.summary(query, sentences=3)
        print('According to Wikipedia,')
        print(results, '\n')
        speak('According to Wikipedia,')
        speak(results)

    elif 'weather' in query:
        print('In which City?')
        speak('In which city?')
        city = takecommand().lower()
        search = f"Weather in {city}"
        url = f"https://www.google.com/search?&q={search}"
        req = requests.get(url)
        sor = BeautifulSoup(req.text, "html.parser")
        temp = sor.find("div", class_='BNeawe').text
        saying = 'Weather in', city, 'is', temp
        print('Weather in', city, 'is', temp)
        speak(saying)

    elif 'open youtube' in query:
        webbrowser.open_new_tab('youtube.com')

    elif 'open stackoverflow' in query or 'open stack overflow' in query:
        webbrowser.open_new_tab('stackoverflow.com')

    elif 'play music' in query:
        music = 'Music'
        songs = os.listdir(music)
        print(songs)
        os.startfile(os.path.join(music, songs[random.randint(0, len(songs)-1)]))

    elif 'time' in query:
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
        print(strtime)
        speak(f"The time is {strtime}")

    elif 'joke' in query:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"}
        )
        if res.status_code == requests.codes.ok:
            print(str(res.json()['joke']))
            speak(str(res.json()['joke']))
        else:
            speak('oops!I ran out of jokes')

    elif "good bye" in query or "bye" in query \
            or "stop" in query or "quit" in query or "close" in query:
        print('Thank you for choosing me ;)')
        speak('Thank you for choosing me')
        quit()

    elif "who i am" in query or "who am i" in query:
        print("If you talk then definitely your human. xD")
        speak("If you talk then definitely your human.")

    elif "notepad" in query:
        speak("Opening Notepad")
        os.system("start Notepad")

    elif "outlook" in query:
        speak("Opening Microsoft Outlook")
        webbrowser.open_new_tab("www.outlook.com")

    elif "word" in query:
        speak("Opening Word")
        os.system("start winword")

    elif "paint" in query:
        speak("Opening Paint")
        os.system("start mspaint")

    elif "excel" in query:
        speak("Opening Excel")
        os.system("start excel")

    elif "chrome" in query:
        speak("Opening Google Chrome")
        os.system("start chrome")

    elif "power point" in query or "powerpoint" in query or "ppt" in query:
        speak("Opening Power Point")
        os.system("start powerpnt")

    elif "edge" in query:
        speak("Opening Microsoft Edge")
        os.system("start msedge")

    elif "snipping tool" in query:
        speak("Opening Snipping Tool")
        os.system("start snippingtool")

    elif "show deleted files" in query or "Recycle Bin" in query \
            or "Delete files" in query or "search deleted files" in query:
        speak("Opening Recycle Bin")
        os.system("start shell:RecycleBinFolder")

    elif "calculator" in query:
        speak("Opening Calculator")
        os.system("start calc")

    elif "i love you" in query:
        speak("It's hard to understand")

    elif 'email' in query:
        global frmsndr
        global frmpass
        # print(frmsndr, frmpass)
        global root2
        root2 = Tk()
        root2.geometry("550x350+450+250")

        ls1 = Label(root2, text='To', width=20, height=3)
        ls2 = Label(root2, text='Subject', width=20, height=3)
        ls3 = Label(root2, text='Body', width=20, height=3)
        ls4 = Label(root2, text='Attach files?', width=20, height=3)
        ls5 = Label(root2, text='File Name', width=20, height=3)

        global es1
        global es2
        global es3

        es1 = Entry(root2, width=50)
        es2 = Entry(root2, width=50)
        es3 = Entry(root2, width=50)

        global es4

        es4 = Text(root2, width=40, height=5)

        Font_tuple = ("Segoe UI", 10)
        es4.configure(font=Font_tuple)

        b = Button(root2, text='Send', width=15, height=3, bg='blue', fg='yellow', activebackground='cyan',
                   activeforeground='red', command=sendemail)

        ls1.grid(row=0, column=0)
        es1.grid(row=0, column=1)
        ls2.grid(row=1, column=0)
        es2.grid(row=1, column=1)
        ls3.grid(row=2, column=0)
        es4.grid(row=2, column=1)
        ls5.grid(row=3, column=0)
        es3.grid(row=3, column=1)
        b.grid(row=4, column=1)

        root2.mainloop()

    elif "where is" in query:
        query = query.replace("where is", "")
        location = query
        speak("User asked to Locate")
        speak(location)
        webbrowser.open("https://www.google.nl/maps/place/" + location + "")

    elif 'created' in query or 'creation' in query:
        print("I was created for SBL Mini Project.")
        speak("I was created for S B L Mini Project.")

    # Writing notes
    elif "write a note" in query or 'write note' in query:
        print("What should i write?")
        speak("What should i write?")
        note = takecommand()
        file = open('notes.txt', 'a')
        print("Should i include date and time?")
        speak("Should i include date and time")
        snfm = takecommand()
        if 'yes' in snfm or 'sure' in snfm:
            strtime = datetime.datetime.now()
            file.write(str(strtime))
            file.write(" :- ")
            file.write(note)
            file.write("\n")
            print('Note Written successfully with Date and Time')
            speak('Note Written successfully with Date and Time')
        else:
            file.write(note)
            file.write("\n")
            print('Note Written successfully')
            speak('Note Written successfully')
        file.close()

    # Showing note
    elif "show note" in query or 'show notes' in query:
        print("Showing Notes")
        speak("Showing Notes")
        file = open("notes.txt", "r")
        print(file.read())
        speak(file.read(6))
        file.close()

    elif "delete note" in query or 'delete a note' in query:
        print("Current Notes")
        speak("Current Notes")
        file = open("notes.txt", "r")
        notes = file.readlines()
        for i in range(len(notes)):
            print(i+1, notes[i], sep='. ')
        print('Say which note to be deleted')
        speak('Say which note to be deleted')
        num = takecommand()
        if num == 'all':
            notes = []
            print("All notes deleted")
            speak("All notes deleted")
        else:
            try:
                notes.pop(int(num)-1)
                print("Note " + num + ' Deleted')
                speak("Note " + num + ' Deleted')
            except:
                print("Sorry I didn't get you... Please retry...")
                speak("Sorry I didn't get you... Please retry...")
        file.close()
        file = open("notes.txt", "w")
        for note in notes:
            print(note, file=file)
        file.close()

    elif 'are you a woman' in query:
        print("I know my voice may fool you, but I don’t have a gender")
        speak("I know my voice may fool you, but I don’t have a gender")

    elif 'do you have children' in query:
        print("As far as I know, none at all")
        speak("As far as I know, none at all")

    elif 'are you foolish' in query:
        print("I’m clever enough to know not to answer")
        speak("I’m clever enough to know not to answer")

    elif 'do you have a favourite song' in query:
        print("My taste in music is quite unconventional... I highly doubt you’d fancy it")
        speak("My taste in music is quite unconventional... I highly doubt you’d fancy it")

    elif 'will you marry me' in query:
        print("My End User Licensing Agreement does not cover that.")
        speak("My End User Licensing Agreement does not cover that.")

    elif 'draw something for me' in query:
        print("I once drew an elephant in space, but no one seemed to get it")
        speak("I once drew an elephant in space, but no one seemed to get it")

    elif 'system' in query or 'system details' in query or 'hardware' in query:
        plat_det = platform.uname()
        print('User : ', plat_det.node)
        print('System :', plat_det.system, plat_det.release,
              plat_det.version)
        print('Machine :', plat_det.machine)
        print('Processor : ', plat_det.processor)
        speak('Users ' + plat_det.node)
        speak('System ' + plat_det.system + plat_det.release + plat_det.version)
        speak('Machine ' + plat_det.machine)
        speak('Processor ' + plat_det.processor)

    elif 'current user' in query:
        print('Currently ' + str(platform.node()) + ' is logged in and has logged in ' +
              str(user_dct[platform.node()]) + ' times till now')
        speak('Currently ' + str(platform.node()) + ' is logged in and has logged in ' +
              str(user_dct[platform.node()]) + ' times till now')


root = Tk()
root.geometry("350x150+500+300")


def micro():
    root.geometry("140x50+200+300")
    global frmsndr
    global frmpass
    frmsndr = ea1.get()
    frmpass = ea2.get()
    for widgets in root.winfo_children():
        widgets.destroy()

    top = Frame(root, height=400, width=500)
    top.pack()
    # Creating a photoimage object to use image
    photo = PhotoImage(file=r"microphone.png")
    # Resizing image to fit on button
    photoimage = photo.subsample(14, 14)
    # Creating a photoimage object to use image
    photo = PhotoImage(file=r"microphone.png")
    B = Button(top, text='Say Something', image=photoimage, compound=LEFT, command=say)
    B.pack()
    root.mainloop()


def hellocallback():
    s1 = e1.get()
    s2 = e2.get()
    if s1 == '' and s2 == '':
        messagebox.showinfo('Welcome', 'Successful Login')

        for widgets in root.winfo_children():
            widgets.destroy()
        fa = Frame(root, height=200, width=400)
        fa.pack()

        la1 = Label(fa, text="E-Mail", width=8, height=2)
        la2 = Label(fa, text="Password", width=8, height=2)

        global ea1
        global ea2
        ea1 = Entry(fa, width=20)
        ea2 = Entry(fa, width=20, show="*")

        ba = Button(fa, text="Login", width=15, height=3, bg='blue', fg='yellow',
                    activebackground='cyan', activeforeground='red', command=micro)

        la1.grid(row=0, column=0)
        ea1.grid(row=0, column=2)
        la2.grid(row=1, column=0)
        ea2.grid(row=1, column=2)
        ba.grid(row=3, column=1)

        messagebox.showinfo("Warning", 'Use the app password rather than your account password')
        root.mainloop()

    else:
        messagebox.showerror('Error', 'Invalid Login')


f = Frame(root, height=350, width=700)
f.pack()

l1 = Label(f, text='Username : ', width=10, height=2)
l2 = Label(f, text='Password : ', width=10, height=2)

e1 = Entry(f, width=20)
e2 = Entry(f, width=20, show='*')

b = Button(f, text='Login', width=15, height=2, bg='blue', fg='yellow', activebackground='cyan',
                   activeforeground='red', command=hellocallback)

l1.grid(row=0, column=0)
e1.grid(row=0, column=2)
l2.grid(row=1, column=0)
e2.grid(row=1, column=2)
b.grid(row=4, column=1)

# For holding the window
root.mainloop()
