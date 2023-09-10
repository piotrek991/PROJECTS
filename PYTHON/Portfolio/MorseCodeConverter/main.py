import pandas as pd

def code(text :str):
    coded= ""
    for letter in text:
        if letter != " ":
            coded += data_dict[letter]+" "
        else:
            coded += "/ "
    return coded[:-1]

def decode(text:str):
    decoded = str()
    to_decode = str()
    #could split like in chek but it works too
    for letter in text:
        if not (letter == " " or letter == "/"):
            to_decode += letter
        else:
            if letter == "/":
                decoded += " "
            else:
                decoded += list(data_dict.keys())[list(data_dict.values()).index(to_decode)]
            to_decode = ""
    decoded += list(data_dict.keys())[list(data_dict.values()).index(to_decode)]
    return decoded


if __name__ == "__main__":
    morse_code_data = pd.read_csv("morse.csv",names=["Letter","Code"])
    data_dict = {key:value for key,value in zip(morse_code_data.Letter,morse_code_data.Code)}

    text_to_convert = input("Word you want to be converted to morse: ").upper()
    morse=False
    if any(c in text_to_convert for c in [".","-"]):
        morse=True
    value_ok = False
    while not value_ok:
        error_occurred = False
        if morse:
            list_letters = text_to_convert.replace("/","").split(" ")
        else:
            list_letters = text_to_convert
        for letter in list_letters:
            try:
                if not morse:
                    test = data_dict[letter]
                else:
                    text = list(data_dict.values()).index(letter)
            except Exception as e:
                print("One of the signs is not valid please input proper text")
                text_to_convert = input("Word you want to be converted to morse: ").upper()
                error_occurred = True
                break
        if not error_occurred:
            value_ok = True

    if morse:
        print(decode(text_to_convert))
    else:
        print(code(text_to_convert))

