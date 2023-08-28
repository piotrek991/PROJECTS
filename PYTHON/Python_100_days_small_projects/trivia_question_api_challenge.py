import requests
import html
from tkinter import *
import random

questions = requests.get("https://opentdb.com/api.php?amount=10&category=18&type=boolean").json()['results']

class QuizInterface:
    def __init__(self):
        self.window = Tk()
        self.score = 0
        self.correct_answer = ""
        self.window.title("Quizlerrr")
        self.window.config(padx=20,pady=20,bg="#375362")
        self.main_image = Canvas(height=250,width=300,bg="white",highlightthickness=0)
        self.question_text = self.main_image.create_text(150,125,width=280,text = "",font=("Arial",20,"italic"))
        self.main_image.grid(column=0,row=1,columnspan=2)

        green_button_image = PhotoImage(file = "./images/true.png")
        self.green_button = Button(image=green_button_image,command = self.true_pressed)
        self.green_button.grid(column=0,row=2,padx = 10,pady =10)

        self.score_text = Label(text=f"Score:{self.score}", font=("Arial"), bg="#375362", fg="white")
        self.score_text.grid(column=1, row=0, pady=(0, 20))

        red_button_image = PhotoImage(file = "./images/false.png")
        self.red_button = Button(image=red_button_image,command = self.false_pressed)
        self.red_button.grid(column=1,row=2,padx = 10,pady =10)

        self.next_question()

        self.window.mainloop()

    def next_question(self):
        global questions
        self.main_image.config(bg="white")
        if len(questions) > 0:
            question = html.unescape(random.choice(questions))
            self.correct_answer = question["correct_answer"]
            self.main_image.itemconfig(self.question_text, text=html.unescape(question["question"]))
            questions.pop(questions.index(question))
        else:
            self.green_button.grid_forget()
            self.red_button.grid_forget()
            self.main_image.itemconfig(self.question_text, text=f"Quiz ended, final score: {self.score}")

    def true_pressed(self):
        if self.correct_answer == "True":
            self.score += 1
            self.score_text.config(text = f"Score:{self.score}")
            self.main_image.config(bg="green")
        else:
            self.main_image.config(bg="red")
        self.window.after(1000,self.next_question)
    def false_pressed(self):
        if self.correct_answer == "False":
            self.score += 1
            self.score_text.config(text = f"Score:{self.score}")
            self.main_image.config(bg="green")
        else:
            self.main_image.config(bg="red")
        self.window.after(1000,self.next_question)


quizui = QuizInterface()
