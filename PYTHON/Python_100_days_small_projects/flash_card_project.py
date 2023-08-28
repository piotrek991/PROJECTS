from tkinter import *
import pandas as pd
import random
import time

current_card = ""

def flip_card():
    try:
        main_area.itemconfig(translation_text, text=data_dictionary[current_card])
    except:
        pass
    else:
        main_area.itemconfig(language_text, text="English")
        main_area.itemconfig(image_container, image=card_back)

def right_answear():
    global session_learned
    global current_card

    session_learned.loc[len(session_learned)] = {"French": current_card, "English": data_dictionary[current_card]}
    session_learned.to_csv("words_learned.csv", index=False)
    data_dictionary.pop(current_card)

    current_card = random.choice(list(data_dictionary.keys()))
    main_area.itemconfig(language_text, text="French")
    main_area.itemconfig(translation_text, text=current_card)
    main_area.itemconfig(image_container, image=card_front)
    window.after(3000, func=flip_card)


def wrong_answear():
    global current_card
    current_card = random.choice(list(data_dictionary.keys()))

    main_area.itemconfig(language_text, text="French")
    main_area.itemconfig(translation_text, text=current_card)
    main_area.itemconfig(image_container, image=card_front)
    window.after(3000,func=flip_card)

BACKGROUND_COLOR = "#B1DDC6"
test_data = pd.read_csv("words_learned.csv")
try:
    session_learned = pd.read_csv("words_learned.csv")
except:
    session_learned = pd.DataFrame(columns=["French", "English"])

data = pd.read_csv("./data/french_words.csv")
data_dictionary = {value.French:value.English for (key,value) in data.iterrows()}
for (index,value) in session_learned.iterrows():
    data_dictionary.pop(value.French)

print(data_dictionary)

window = Tk()
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

current_card = random.choice(list(data_dictionary.keys()))
window.after(3000,func=flip_card)

main_area = Canvas(height = 526,width = 800,bg = BACKGROUND_COLOR,highlightthickness=0)
card_front = PhotoImage(file = "./images/card_front.png")
card_back = PhotoImage(file = "./images/card_back.png")
image_container = main_area.create_image(410,263, image = card_front)


language_text = main_area.create_text(400,150,text = "French", font=("Ariel",40,"italic"))
translation_text = main_area.create_text(400,263,text =current_card , font=("Ariel",60,"bold"))
main_area.grid(column = 0,row = 0,columnspan=2)

red_image = PhotoImage(file="./images/wrong.png")
green_image = PhotoImage(file="./images/right.png")
button_red = Button(image=red_image,command = wrong_answear(),highlightthickness=0)
button_green = Button(image=green_image,command = right_answear,highlightthickness=0)

button_red.grid(column=0,row=1)
button_green.grid(column=1,row=1)
window.mainloop()

