from tkinter import *
import random

def generate_pass():
    final = []
    text_final = ""
    for i in range(0,3):
        final.append(random.randint(0,9))
    for i in range(0,10):
        letter = chr(random.randint(65,122))
        while(not letter.isalpha()):
            letter = chr(random.randint(65, 122))
        final.append(letter)
    for i in range(0,2):
        letter = chr(random.randint(33, 126))
        while (letter.isalpha() or letter.isdigit()):
            letter = chr(random.randint(33, 126))
        final.append(letter)
    final = random.sample(final,len(final))
    for item in final:
        if str(item).isdigit():
            text_final += str(item)
            continue
        text_final += item
    input_password.delete(0,'end')
    input_password.insert(0,text_final)


def add_password():
    text_to_write = input_website.get() + " | " + input_login.get() + " | " + input_password.get() + "\n"
    with open("paswords.txt","a") as file:
        file.write(text_to_write)
        file.close()

window = Tk()
window.title("Password Manager")
window.config(padx = 20, pady = 50,bg = "white")

canvas = Canvas(width=200,height=200,bg = "white", highlightthickness = 0)
label_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=label_img)
canvas.grid(column=1,row=1)

website_label = Label(text = "Website:",bg="white",font=("Arial",14))
website_label.grid(column=0,row=2)
input_website = Entry(width=55)
input_website.grid(column=1,row=2,columnspan=2,sticky="w")

login_label = Label(text = "Login/Username:",bg="white",font=("Arial",14))
login_label.grid(column=0,row=3)
input_login = Entry(width=55)
input_login.grid(column=1,row=3,columnspan=2,sticky="w")

password_label = Label(text = "Password:",bg="white",font=("Arial",14))
password_label.grid(column=0,row=4)
input_password = Entry(width=30)
input_password.grid(column=1,row=4,sticky="w")

generate_pass_button = Button(text="Generate Password", command= generate_pass,font = ("Arial",8),height=1)
generate_pass_button.grid(column=2,row=4,sticky="n")

add_button = Button(text="Add", command= add_password,width=75)
add_button.grid(column=0,row=5,columnspan = 3)


window.mainloop()
