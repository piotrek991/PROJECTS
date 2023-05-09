# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    first_number = 0
    row_string = ""
    for i in range(10):
        for x in range(first_number,10):
            row_string = row_string + str(x)
        for y in range(0, first_number):
            row_string = row_string + str(y)
        first_number+=1
        print(f"{row_string}")
        row_string = ""

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
