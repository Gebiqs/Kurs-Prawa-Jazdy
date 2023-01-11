import pandas as pd
import random
import tkinter, threading
from PIL import ImageTk, Image
from tkVideoPlayer import TkinterVideo
import traceback
from pathlib import Path

start_button, restart_button,a,b,c,t,n,header,current_question,label,myLabel, score, question_number =0,0,0,0,0,0,0,0,0,0,0,0,0

#wczytywanie pliku jako start
df = pd.read_excel(f"{Path().absolute()}/PRAWOJAZDY/!pytania_plik_październik_2018 (1).xlsm".format())
df = df[df['Kategorie'].str.contains('B').fillna(False)]
df = df[~df['Media'].str.contains('.wmv').fillna(False)] #obecnie wyłączone są video przez brak kompatybilności z formatem siatki (szukane obejście)
df = df[df['Media'].notna()]

#załadowanie okna
root = tkinter.Tk()
root.title("Prawo jazdy")
root.geometry("800x700")
root.resizable(width=False, height=False)

#konfiguracja siatki
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(3, weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=3)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)
root.rowconfigure(4,weight=1)


def restart_window():   #usuwanie poprzedniego tekstu, obrazu, odpowiedzi i przycisku do restartu
    global start_button, restart_button,a,b,c,t,n,header,current_question, label, myLabel, clicks_counter, question_number
    del current_question
    for i in [start_button, restart_button,a,b,c,t,n,header, label, myLabel]:
        try:
            i.destroy()
        except:
            pass
    clicks_counter = 0
    question_number+= 1


def generate_new_header(current_question):  #generowanie nowego tekstu
    global header
    header = tkinter.Label(root, text=current_question.iloc[0, 2], font="Calibri", padx=20,pady=20, wraplength=780)
    header.grid(row =0, column=0, columnspan=3)


def generate_picture(current_question):     #generowanie nowego obrazu
    global image, label

    file_path = current_question.iloc[0, 15]
    file_extension = file_path[len(file_path)-3:]
    if file_extension == "jpg":
        image = Image.open(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{current_question.iloc[0, 15]}".format())
        image = image.resize((800, 400))
        image = ImageTk.PhotoImage(image)
        label = tkinter.Label(root, image=image)
        label.grid(row=1, column=0, columnspan=3)

    if file_extension in ("mp4","wmv"):
        #formaty plików w ścieżkach nie zgadzają się z rzeczywistymi plikami w bazie danych
        videoplayer = TkinterVideo(master=root,scaled=False)
        videoplayer.set_size((1200,1200))
        try:
            videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path[:len(file_path)-3]}mp4")
            videoplayer.grid(row=1, column=0, columnspan=3)
            videoplayer.play()
        except:
            try:
                traceback.print_exc()
                videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path}")
                videoplayer.grid(row=1, column=0, columnspan=3)
                videoplayer.play()
            except:
                videoplayer.load(f"D:\Pliki python\Kurs prawo jazdy\PRAWOJAZDY\{file_path[:len(file_path)-3]}wmv")
                videoplayer.grid(row=1, column=0, columnspan=3)
                videoplayer.play()

def generate_score():
    my_score = tkinter.Label(root, text=f"Pytanie #{question_number}\n\nWynik:\n{score}/{question_number-1}".format())
    my_score.grid(row=3, column=0)


def check_answer(ans,current_question): #f. sprawdzająca poprawność odpowiedzi
    global myLabel, clicks_counter, score
    if myLabel !=0:
        myLabel.destroy()
    if current_question.iloc[0,14]==ans:
        myLabel = tkinter.Label(root, text="Dobrze")
        myLabel.grid(row=2,column=0)
        if clicks_counter==0:
            score+=1
    else:
        myLabel = tkinter.Label(root, text="Źle")
        myLabel.grid(row=2,column=0)
    clicks_counter += 1 #przy każdym kliknięciu w jednej pętli zwiększamy counter o 1


def generate_answers(current_question): #generowanie noweych odpowiedzi w wariancie T/N, ABC
    global a,b,c,t,n
    #pytania T/F
    if current_question.iloc[0,14] in ("T","N"):
        t = tkinter.Button(root, text="Prawda", command= lambda: check_answer("T",current_question))     #width=60, height=5,
        n = tkinter.Button(root, text="Fałsz",command= lambda: check_answer("N",current_question))       #width=60, height=5,
        t.grid(row=2,column=1)
        n.grid(row=3,column=1)

    #jeśli pytania ABC
    elif current_question.iloc[0,14] in ("A","B","C"): #poprawna odpowiedź
        a = tkinter.Button(root, text=f"{current_question.iloc[0, 3]}".format(), command= lambda: check_answer("A",current_question)) #Odpowiedź A #width=60, height=5,
        b = tkinter.Button(root, text=f"{current_question.iloc[0, 4]}".format(), command= lambda: check_answer("B",current_question)) #Odpowiedź B #width=60, height=5,
        c = tkinter.Button(root,  text=f"{current_question.iloc[0, 5]}".format(), command= lambda: check_answer("C",current_question)) #Odpowiedź C #width=60, height=5,
        a.grid(row=2,column=1)
        b.grid(row=3,column=1)
        c.grid(row=4,column=1)


def main():
    global restart_button, current_question
    try:
        start_button.destroy()
    except:
        pass
    restart_window()
    current_question = df.iloc[[random.randint(1, len(df) - 1)]]
    generate_new_header(current_question)
    generate_picture(current_question)
    generate_answers(current_question)
    generate_score()
    restart_button = tkinter.Button(root, text="Następne pytanie", width=25, height=18, command=main)
    restart_button.grid(row=2,column=2, rowspan=3)


current_question = df.iloc[[random.randint(1, len(df))]]

#przycisk do startu w oknie startowym
restart_button = tkinter.Button(root, text="Następne pytanie", width=50, height=10, command=main)
start_button = tkinter.Button(root, text="Rozpocznij", width=60, height=20,command=main)
start_button.grid(row=1,column=1)


root.mainloop()