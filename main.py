import pandas as pd
import random
import tkinter, threading
from PIL import ImageTk, Image
from tkVideoPlayer import TkinterVideo
import traceback
from pathlib import Path

start_button, restart_button,a,b,c,t,n,header,current_question,label,myLabel, score, question_number, videoplayer =0,0,0,0,0,0,0,0,0,0,0,0,0,0

#wczytywanie pliku jako start
df = pd.read_excel(f"{Path().absolute()}/PRAWOJAZDY/!pytania_plik_październik_2018 (1).xlsm".format())
df = df[df['Kategorie'].str.contains('B').fillna(False)]
#df = df[~df['Media'].str.contains('.wmv').fillna(False)] #obecnie wyłączone są video przez brak kompatybilności z formatem siatki (szukane obejście)
df = df[df['Media'].notna()]

#załadowanie okna
root = tkinter.Tk()
root.title("Prawo jazdy")
root.attributes("-fullscreen", True)

"""
def place_background_image():
    global bg, tło
    bg = ImageTk.PhotoImage(file="tło.png")
    tło = tkinter.Label(root, image=bg)
    tło.place(x=-1, y=-1)

place_background_image()
"""


def restart_window():   #usuwanie poprzedniego tekstu, obrazu, odpowiedzi i przycisku do restartu
    global start_button, restart_button,a,b,c,t,n,header,current_question, label, myLabel, clicks_counter, question_number, videoplayer #tło
    del current_question
    for i in [start_button, restart_button,a,b,c,t,n,header, label, myLabel, videoplayer]: #,tło]:
        try:
            i.destroy()
        except:
            pass
    clicks_counter = 0
    question_number+= 1


def generate_new_header(current_question):  #generowanie nowego tekstu
    global header
    header = tkinter.Label(root, text=current_question.iloc[0, 2], font="Calibri", padx=20,pady=20, wraplength=780)
    header.place(relx=0.5,rely=0.185, anchor="center")


def generate_picture(current_question):     #generowanie nowego obrazu
    global image, label, videoplayer

    file_path = current_question.iloc[0, 15]
    file_extension = file_path[len(file_path)-3:]
    if file_extension == "jpg":
        image = Image.open(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{current_question.iloc[0, 15]}".format())
        image = image.resize((800, 400))
        image = ImageTk.PhotoImage(image)
        label = tkinter.Label(root, image=image)
        label.pack(expand=True, fill="both")

    if file_extension in ("mp4","wmv"):
        #formaty plików w ścieżkach nie zgadzają się z rzeczywistymi plikami w bazie danych
        videoplayer = TkinterVideo(master=root,scaled=False)
        videoplayer.set_size((800,450))
        try:
            videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path[:len(file_path)-3]}mp4")
            videoplayer.pack(expand=True, fill="both")
            videoplayer.play()
        except:
            try:
                traceback.print_exc()
                videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path}")
                videoplayer.pack(expand=True, fill="both")
                videoplayer.play()
            except:
                videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path[:len(file_path)-3]}wmv")
                videoplayer.pack(expand=True, fill="both")
                videoplayer.play()

def generate_score():
    my_score = tkinter.Label(root, text=f"Pytanie #{question_number}\n\nWynik:\n{score}/{question_number-1}", font="calibri")
    my_score.place(relx=0.25,rely=0.8611, anchor="center")

def check_answer(ans,current_question): #f. sprawdzająca poprawność odpowiedzi
    global myLabel, clicks_counter, score
    if myLabel !=0:
        myLabel.destroy()
    if current_question.iloc[0,14]==ans:
        myLabel = tkinter.Label(root, text="Dobrze", font="calibri")
        myLabel.place(relx=0.25,rely=0.93, anchor="center")
        if clicks_counter==0:
            score+=1
    else:
        myLabel = tkinter.Label(root, text="Źle", font="calibri")
        myLabel.place(relx=0.25,rely=0.93, anchor="center")
    clicks_counter += 1 #przy każdym kliknięciu w jednej pętli zwiększamy counter o 1


def generate_answers(current_question): #generowanie noweych odpowiedzi w wariancie T/N, ABC
    global a,b,c,t,n
    #pytania T/F
    if current_question.iloc[0,14] in ("T","N"):
        t = tkinter.Button(root, text="Prawda", font="calibri", command= lambda: check_answer("T",current_question))
        n = tkinter.Button(root, text="Fałsz", font="calibri",command= lambda: check_answer("N",current_question))
        t.place(relx=0.5,rely=0.815, anchor="center",width=120, height=50)
        n.place(relx=0.5,rely=0.90, anchor="center", width=120, height=50)

    #jeśli pytania ABC
    elif current_question.iloc[0,14] in ("A","B","C"): #poprawna odpowiedź
        a = tkinter.Button(root, text=f"{current_question.iloc[0, 3]}".format(), font="calibri", wraplength=380, command= lambda: check_answer("A",current_question))
        b = tkinter.Button(root, text=f"{current_question.iloc[0, 4]}".format(), font="calibri", wraplength=380, command= lambda: check_answer("B",current_question))
        c = tkinter.Button(root,  text=f"{current_question.iloc[0, 5]}".format(), font="calibri", wraplength=380, command= lambda: check_answer("C",current_question))
        a.place(relx=0.5,rely=0.7686, anchor="center", width=400, height=55)
        b.place(relx=0.5,rely=0.861, anchor="center", width=400, height=55)
        c.place(relx=0.5,rely=0.954, anchor="center", width=400, height=55)


def main():
    global restart_button, current_question #, tło
    try:
        start_button.destroy()
    except:
        pass
    restart_window()
    current_question = df.iloc[[random.randint(1, len(df) - 1)]]
    #place_background_image()
    generate_picture(current_question)

    generate_new_header(current_question)
    generate_answers(current_question)
    generate_score()
    restart_button = tkinter.Button(root, text="Następne pytanie", font="calibri", width=25, height=8, command=main)
    restart_button.place(relx=0.75,rely=0.8611, anchor="center")


current_question = df.iloc[[random.randint(1, len(df))]]

#przycisk do startu w oknie startowym
#restart_button = tkinter.Button(root, text="Następne pytanie", font="calibri", width=50, height=10, command=main)
start_button = tkinter.Button(root, text="Rozpocznij", font="calibri", width=60, height=20,command=main)
start_button.place(relx=0.5,rely=0.5, anchor="center")


root.mainloop()