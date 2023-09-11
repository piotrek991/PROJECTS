import tkinter
from tkinter import *
from PIL import Image,ImageTk
import pandas as pd
from datetime import datetime
import random

time_start = datetime.now()
type_time = datetime.now()
def check_text(e):
    global first
    global last
    global time_start
    global type_time
    if first:
        first = False
        time_start = datetime.now()

    if e.char or e.keysym == 'BackSpace':
        index = int(input_text.index(tkinter.INSERT).split(".")[-1])
        actual = input_text.get("1.0", 'end-1c')
        taggers = [tag.string for tag in input_text.tag_ranges("start")]
        if taggers:
            input_text.tag_remove("start","1."+str(index),"1."+str(len(actual)))

        for i in range(index-1,len(actual)):
            text1 = "1." + str(i)
            text2 = "1." + str(i + 1)
            if sample_quote[i] != actual[i]:
                input_text.tag_add("start",text1,text2)
        if len(actual) == len(sample_quote) and not taggers:
            if not last:
                last = True
                type_time = datetime.now()-time_start
            print(type_time)
            input_text.configure(state="disabled")
            wpm = (len(sample_quote.split(" ")) / (type_time.seconds + type_time.microseconds/10**6))*60
            result.configure(text=f"Input type finished, calculated WPM: {wpm}")

data = pd.read_csv("Quotes.csv",delimiter=";")
quotes = list(data.QUOTE)
first,last = True,False

window = Tk()
window.title("Typing speed meter")
window.config(padx=20 ,pady=50, bg="white")


canvas = Canvas(width=400,height=300,bg="white", highlightthickness=0)
logo_image = Image.open("keyboard.png").resize((350,250))
new_image = ImageTk.PhotoImage(logo_image)
canvas.create_image(200,150,image=new_image)
canvas.grid(column=1, row=1)

sample_quote = random.choice(quotes)
text_to_type = Label(text=sample_quote,bg="white",font = ("Arial",14))
text_to_type.grid(column=1,row=2)

input_text = Text(window, width=int(0.8*len(text_to_type.cget("text"))),height = 1, font = ("Arial",14))
input_text.grid(column=1,row=3)
input_text.bind('<KeyRelease>',check_text)
input_text.tag_config("start",foreground="red")

result = Label(text=str(),bg="white",font = ("Arial",14))
result.grid(column=1,row=4)

window.mainloop()