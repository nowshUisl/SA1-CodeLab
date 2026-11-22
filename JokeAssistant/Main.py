
import tkinter as tk
from tkinter import messagebox
import random
import os


# Colours
BG = "#111827"
PANEL = "#1F2937"
CARD = "#273449"
BLUE = "#38BDF8"
WHITE = "#F9FAFB"
GREY = "#9CA3AF"
YELLOW = "#FACC15"


# Load jokes from the text file
def load_jokes():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "randomJokes.txt"
    )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            jokes = file.readlines()

        return [joke.strip() for joke in jokes if "?" in joke]

    except FileNotFoundError:
        messagebox.showerror("Error", "randomJokes.txt was not found!")
        return []


current_punchline = ""


# Display a random joke
def tell_joke():
    global current_punchline

    if not jokes:
        messagebox.showwarning("No Jokes", "No jokes available!")
        return

    joke = random.choice(jokes)
    setup, current_punchline = joke.split("?", 1)

    setup_label.config(text=setup.strip() + "?")
    punchline_label.config(text="")

    punchline_button.config(state="normal")
    status_label.config(text="Can you guess the punchline?")


# Show the punchline
def show_punchline():
    if current_punchline:
        punchline_label.config(text=current_punchline.strip())
        status_label.config(text="Here's the answer!")


# Get another joke
def next_joke():
    tell_joke()


# Main window
window = tk.Tk()
window.title("Joke Telling Assistant")
window.geometry("550x470")
window.resizable(False, False)
window.config(bg=BG)


# Load jokes after creating the window
jokes = load_jokes()


# Main heading
title_label = tk.Label(
    window,
    text="JOKE TIME",
    font=("Arial", 25, "bold"),
    bg=BG,
    fg=WHITE
)
title_label.pack(pady=(25, 5))


subtitle_label = tk.Label(
    window,
    text="A little laughter goes a long way",
    font=("Arial", 11),
    bg=BG,
    fg=GREY
)
subtitle_label.pack(pady=(0, 20))


# Main joke panel
joke_frame = tk.Frame(
    window,
    bg=PANEL,
    padx=25,
    pady=25
)
joke_frame.pack(padx=35, fill="both", expand=True)


# Small heading inside panel
question_heading = tk.Label(
    joke_frame,
    text="YOUR RANDOM JOKE",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=BLUE
)
question_heading.pack(pady=(5, 20))


# Joke question
setup_label = tk.Label(
    joke_frame,
    text="Click below to get your first joke!",
    font=("Arial", 15, "bold"),
    bg=PANEL,
    fg=WHITE,
    wraplength=420,
    justify="center"
)
setup_label.pack(pady=10)


# Punchline
punchline_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=YELLOW,
    wraplength=420,
    justify="center"
)
punchline_label.pack(pady=15)


# Status message
status_label = tk.Label(
    joke_frame,
    text="Ready for a laugh?",
    font=("Arial", 10),
    bg=PANEL,
    fg=GREY
)
status_label.pack(pady=5)


# Buttons
button_frame = tk.Frame(
    window,
    bg=BG
)
button_frame.pack(pady=20)


# Tell joke button
tell_button = tk.Button(
    button_frame,
    text="Tell Me a Joke",
    font=("Arial", 11, "bold"),
    bg=BLUE,
    fg=BG,
    activebackground="#0EA5E9",
    activeforeground=WHITE,
    relief="flat",
    width=17,
    pady=10,
    cursor="hand2",
    command=tell_joke
)
tell_button.grid(row=0, column=0, padx=6)


# Show punchline button
punchline_button = tk.Button(
    button_frame,
    text="Show Punchline",
    font=("Arial", 11, "bold"),
    bg=CARD,
    fg=WHITE,
    activebackground="#37465C",
    activeforeground=WHITE,
    relief="flat",
    width=17,
    pady=10,
    cursor="hand2",
    state="disabled",
    command=show_punchline
)
punchline_button.grid(row=0, column=1, padx=6)


# Next joke button
next_button = tk.Button(
    window,
    text="NEXT JOKE  →",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=BLUE,
    activebackground=BG,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=next_joke
)
next_button.pack(pady=(0, 5))


# Quit button
quit_button = tk.Button(
    window,
    text="EXIT",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=GREY,
    activebackground=BG,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=window.destroy
)
quit_button.pack(pady=(0, 10))


# Run the program
window.mainloop()
