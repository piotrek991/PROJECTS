from tkinter import *
import time
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    count_down(5*60)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(time):
    count_min,count_sec = divmod(time, 60)
    text_ = "{:02d}:{:02d}".format(count_min,count_sec)
    canvas.itemconfig(time_label, text = text_)
    if time > 0:
        window.after(1000,count_down,time-1)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=200,pady=50,bg=YELLOW)

my_label = Label(text="TIMER",fg=GREEN,bg=YELLOW, font=(FONT_NAME,30,"bold"))
my_label.grid(column=1,row=0)

canvas = Canvas(width=200, height=224,bg=YELLOW,highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100,112, image = tomato_img)
time_label = canvas.create_text(100,130, text="00:00",fill="white",font=(FONT_NAME,35,"bold"))
canvas.grid(column=1,row=1)

button_start = Button(text = "Start",command = start_timer)
button_start.grid(column=0,row=2)
button_start = Button(text = "Reset",command = start_timer)
button_start.grid(column=2,row=2)



window.mainloop()