import tkinter as tk
from tkinter import ttk
from enum import Enum

class RadioApp():
    class Test(Enum):
        TEST1 = 'TEST'
        def __str__(self):
            return str(self.value)
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")

        # Create a variable to store the selected option
        self.selected_option = tk.StringVar()
        # Optionally set a default value
        self.selected_option.set("Option 1")

        # Label to display the selected option
        self.label = ttk.Label(self.root, text="Selected: None")
        self.label.pack(pady=10)

        # List of radio button options
        options = [("Option 1", "Option 1"),
                   ("Option 2", "Option 2"),
                   ("Option 3", "Option 3")]

        # Create radio buttons
        for text, value in options:
            radio = ttk.Radiobutton(
                self.root,
                text=text,
                value=value,
                variable=self.selected_option,
                command=self.update_label
            )
            radio.pack(anchor="w", padx=20, pady=5)

        # Button to quit the app
        quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)

    def update_label(self):
        # Update the label with the selected option
        self.label.config(text=f"Selected: {self.selected_option.get()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RadioApp(root)
    print(app.Test.TEST1.name)
    root.mainloop()