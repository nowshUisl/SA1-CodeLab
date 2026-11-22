
import tkinter as tk
import random

# COLOURS AND FONTS

BG = "#10111F"
PANEL = "#1B1D32"
PANEL2 = "#252842"
PURPLE = "#9B5CFF"
CYAN = "#00E5FF"
WHITE = "#FFFFFF"
GREY = "#A5A8C5"
GREEN = "#42E6A4"
RED = "#FF5573"
ORANGE = "#FFB454"
FONT = "Segoe UI"

# QUIZ VARIABLES

score = 0
question_number = 0
total_questions = 10
attempts = 0
correct_answer = 0
difficulty = ""
answered = False
after_id = None
current_screen = "menu"

# MAIN WINDOW

root = tk.Tk()
root.title("Math Challenge")
root.geometry("700x850")
root.resizable(False, False)
root.configure(bg=BG)

# ROUNDED RECTANGLE FUNCTION

# Draws a rounded rectangle using a Canvas polygon.
# This allows the application to have rounded panels and buttons.
def rounded_rectangle(canvas, x1, y1, x2, y2, radius, colour, tag=None):

    if x2 <= x1 or y2 <= y1:
        return

    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)

    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=24,
        fill=colour,
        outline=colour,
        tags=tag
    )

# ROUNDED PANEL CLASS

# Creates a reusable rounded panel for different application screens.
class RoundedPanel(tk.Frame):

    def __init__(self, parent, width, height, colour=PANEL):

        super().__init__(parent, width=width, height=height, bg=BG)

        self.pack_propagate(False)

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=BG,
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        rounded_rectangle(
            self.canvas, 2, 2, width - 2, height - 2,
            25, colour
        )

        self.content = tk.Frame(self, bg=colour)
        self.content.place(
            x=12, y=12,
            width=width - 24,
            height=height - 24
        )

# ROUNDED BUTTON CLASS

# Creates buttons with rounded corners and hover effects.
class RoundedButton(tk.Frame):

    def __init__(
        self, parent, text, command,
        width=300, height=50,
        colour=PURPLE,
        hover_colour="#7540C4",
        text_colour=WHITE,
        font=(FONT, 13, "bold")
    ):

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg")
        )

        self.pack_propagate(False)

        self.command = command
        self.normal_colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.text = text
        self.font = font
        self.enabled = True

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True)

        self.draw_button(colour)

        # Connects mouse movements and clicks to the button.
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.on_click)

    # Draws the button with its current colour and text.
    def draw_button(self, colour):

        self.canvas.delete("all")

        width = int(self.canvas["width"])
        height = int(self.canvas["height"])

        rounded_rectangle(
            self.canvas, 1, 1, width - 1, height - 1,
            17, colour
        )

        self.canvas.create_text(
            width // 2,
            height // 2,
            text=self.text,
            fill=self.text_colour,
            font=self.font
        )

    # Changes the button colour when the mouse enters.
    def on_enter(self, event):

        if self.enabled:
            self.draw_button(self.hover_colour)

    # Restores the original colour when the mouse leaves.
    def on_leave(self, event):

        if self.enabled:
            self.draw_button(self.normal_colour)

    # Runs the button's assigned command when clicked.
    def on_click(self, event):

        if self.enabled:
            self.command()

    # Enables or disables the button during the quiz.
    def set_enabled(self, enabled):

        self.enabled = enabled

        if enabled:
            self.draw_button(self.normal_colour)
        else:
            self.draw_button("#45455A")

# ROUNDED ANSWER ENTRY CLASS

# Creates a styled answer box inside a rounded purple border.
class RoundedEntry(tk.Frame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=300,
            height=55,
            bg=PANEL
        )

        self.pack_propagate(False)

        self.canvas = tk.Canvas(
            self,
            width=300,
            height=55,
            bg=PANEL,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        rounded_rectangle(
            self.canvas, 1, 1, 299, 54,
            15, PURPLE
        )

        rounded_rectangle(
            self.canvas, 3, 3, 297, 52,
            13, PANEL2
        )

        self.entry = tk.Entry(
            self.canvas,
            font=(FONT, 20, "bold"),
            justify="center",
            bg=PANEL2,
            fg=CYAN,
            insertbackground=CYAN,
            relief="flat",
            bd=0
        )

        self.canvas.create_window(
            150, 27,
            width=270,
            height=35,
            window=self.entry
        )

        self.entry.bind(
            "<Button-1>",
            lambda event: self.entry.focus_force()
        )

# PROGRESS BAR

# Updates the progress bar according to the current question number.
def update_progress():

    progress_bar.delete("fill")

    fill_width = 430 * question_number / total_questions

    if fill_width > 0:
        rounded_rectangle(
            progress_bar,
            0, 0,
            fill_width, 14,
            7, CYAN,
            tag="fill"
        )

# SCREEN MANAGEMENT

# Cancels a scheduled question change when leaving the quiz screen.
def cancel_pending():

    global after_id

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None


# Hides all three main screens before displaying another one.
def clear_screens():

    menu_frame.pack_forget()
    quiz_frame.pack_forget()
    results_frame.pack_forget()


# Returns the user to the difficulty selection menu.
def display_menu():

    global current_screen

    cancel_pending()
    current_screen = "menu"

    clear_screens()
    menu_frame.pack(pady=15)

# DIFFICULTY SELECTION

# Stores the selected difficulty and starts a new quiz.
def select_difficulty(level):

    global difficulty, current_screen

    difficulty = level
    current_screen = "quiz"

    clear_screens()
    quiz_frame.pack(pady=5)

    start_quiz()


# Returns to the main menu using the back button.
def go_back():

    display_menu()

# START QUIZ

# Resets the score and question counter before starting.
def start_quiz():

    global score, question_number, answered

    score = 0
    question_number = 0
    answered = False

    update_score()
    next_question()

# GENERATE QUESTIONS

# Generates random addition or subtraction questions.
# The number range depends on the selected difficulty.
def next_question():

    global question_number, attempts
    global correct_answer, answered, after_id

    after_id = None

    if current_screen != "quiz":
        return

    # Displays the results after all ten questions.
    if question_number >= total_questions:
        display_results()
        return

    question_number += 1
    attempts = 0
    answered = False

    if difficulty == "Easy":
        minimum, maximum = 1, 9

    elif difficulty == "Moderate":
        minimum, maximum = 10, 99

    else:
        minimum, maximum = 1000, 9999

    num1 = random.randint(minimum, maximum)
    num2 = random.randint(minimum, maximum)

    operation = random.choice(["+", "-"])

    if operation == "+":
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2

    question_label.config(text=f"{num1}  {operation}  {num2}")

    question_count_label.config(
        text=f"QUESTION {question_number:02d} / 10"
    )

    update_progress()

    answer_entry.entry.config(state="normal")
    answer_entry.entry.delete(0, tk.END)

    submit_button.set_enabled(True)

    feedback_label.config(
        text="ENTER YOUR ANSWER BELOW",
        fg=GREY
    )

    # Automatically places the cursor inside the answer box.
    root.after(100, answer_entry.entry.focus_force)

# CHECK ANSWER

# Checks the user's answer and awards points.
# The user gets two attempts for each question.
def check_answer():

    global attempts, score, answered, after_id

    if current_screen != "quiz" or answered:
        return

    user_input = answer_entry.entry.get().strip()

    if user_input == "":
        feedback_label.config(
            text="PLEASE ENTER AN ANSWER",
            fg=RED
        )
        answer_entry.entry.focus_force()
        return

    # Makes sure the answer contains a valid integer.
    try:
        user_answer = int(user_input)

    except ValueError:
        feedback_label.config(
            text="PLEASE ENTER A VALID NUMBER",
            fg=RED
        )
        answer_entry.entry.delete(0, tk.END)
        answer_entry.entry.focus_force()
        return

    attempts += 1

    if user_answer == correct_answer:

        answered = True

        # Awards more points for answering correctly on the first attempt.
        if attempts == 1:
            score += 10
            feedback_label.config(
                text="CORRECT! +10 POINTS",
                fg=GREEN
            )
        else:
            score += 5
            feedback_label.config(
                text="CORRECT! +5 POINTS",
                fg=GREEN
            )

        update_score()

        answer_entry.entry.config(state="disabled")
        submit_button.set_enabled(False)

        # Moves to the next question after a short delay.
        after_id = root.after(1100, next_question)

    else:

        if attempts == 1:

            feedback_label.config(
                text="WRONG! TRY AGAIN",
                fg=ORANGE
            )

            answer_entry.entry.delete(0, tk.END)
            answer_entry.entry.config(state="normal")
            answer_entry.entry.focus_force()

        else:

            answered = True

            # Displays the correct answer after the second wrong attempt.
            feedback_label.config(
                text=f"CORRECT ANSWER: {correct_answer}",
                fg=RED
            )

            answer_entry.entry.config(state="disabled")
            submit_button.set_enabled(False)

            after_id = root.after(1600, next_question)

# UPDATE SCORE

# Updates the score display whenever points are awarded.
def update_score():

    score_label.config(text=f"{score:03d}")

# RESULTS SCREEN

# Displays the final score, grade and performance message.
def display_results():

    global current_screen

    current_screen = "results"

    clear_screens()
    results_frame.pack(pady=25)

    # Selects a grade based on the final score.
    if score >= 90:
        grade = "S"
        message = "LEGENDARY PERFORMANCE!"

    elif score >= 80:
        grade = "A"
        message = "EXCELLENT WORK!"

    elif score >= 70:
        grade = "B"
        message = "GREAT JOB!"

    elif score >= 60:
        grade = "C"
        message = "GOOD EFFORT!"

    elif score >= 50:
        grade = "D"
        message = "KEEP PRACTISING!"

    else:
        grade = "F"
        message = "YOU CAN DO BETTER!"

    result_grade.config(text=grade)
    result_score.config(text=f"{score} / 100")
    result_message.config(text=message)

# REPLAY AND EXIT

# Returns to the menu so the user can select another difficulty.
def replay_quiz():

    display_menu()


# Closes the application and cancels any pending question changes.
def exit_quiz():

    cancel_pending()
    root.destroy()

# HEADER DESIGN

header = tk.Frame(root, bg=BG)
header.pack(pady=(10, 5))

tk.Label(
    header,
    text="NEON",
    font=(FONT, 16, "bold"),
    fg=CYAN,
    bg=BG
).pack()

tk.Label(
    header,
    text="MATH CHALLENGE",
    font=(FONT, 27, "bold"),
    fg=WHITE,
    bg=BG
).pack()

tk.Label(
    header,
    text="THINK FAST. SOLVE SMART. SCORE BIG.",
    font=(FONT, 9, "bold"),
    fg=GREY,
    bg=BG
).pack(pady=3)

# MENU SCREEN

menu_frame = RoundedPanel(root, 500, 430, PANEL)
menu_content = menu_frame.content

tk.Label(
    menu_content,
    text="SELECT YOUR LEVEL",
    font=(FONT, 22, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(pady=(35, 8))

tk.Label(
    menu_content,
    text="Choose a difficulty to begin",
    font=(FONT, 12),
    bg=PANEL,
    fg=GREY
).pack(pady=(0, 25))


# Creates a difficulty button that starts the selected level.
def create_difficulty_button(text, level, colour):

    button = RoundedButton(
        menu_content,
        text=text,
        command=lambda: select_difficulty(level),
        width=320,
        height=55,
        colour=colour,
        hover_colour="#454966"
    )

    button.pack(pady=10)


create_difficulty_button("01   EASY", "Easy", "#168C83")
create_difficulty_button("02   MODERATE", "Moderate", "#5365D9")
create_difficulty_button("03   ADVANCED", "Advanced", "#8846D9")

# QUIZ SCREEN

quiz_frame = RoundedPanel(root, 550, 650, PANEL)
quiz_content = quiz_frame.content

# Back button allows the user to leave the quiz at any time.
back_button = RoundedButton(
    quiz_content,
    text="←  BACK TO MENU",
    command=go_back,
    width=180,
    height=38,
    colour=RED,
    hover_colour="#D93659",
    font=(FONT, 11, "bold")
)
back_button.pack(anchor="w", pady=(3, 5))

question_count_label = tk.Label(
    quiz_content,
    text="QUESTION 01 / 10",
    font=(FONT, 11, "bold"),
    bg=PANEL,
    fg=CYAN
)
question_count_label.pack(pady=5)

# QUIZ PROGRESS BAR

progress_bar = tk.Canvas(
    quiz_content,
    width=430,
    height=14,
    bg=PANEL2,
    highlightthickness=0
)
progress_bar.pack(pady=8)

rounded_rectangle(progress_bar, 0, 0, 430, 14, 7, PANEL2)

# SCORE DISPLAY

score_panel = RoundedPanel(quiz_content, 200, 85, PANEL2)
score_panel.pack(pady=10)

tk.Label(
    score_panel.content,
    text="CURRENT SCORE",
    font=(FONT, 9, "bold"),
    bg=PANEL2,
    fg=GREY
).pack(pady=(7, 0))

score_label = tk.Label(
    score_panel.content,
    text="000",
    font=(FONT, 26, "bold"),
    bg=PANEL2,
    fg=CYAN
)
score_label.pack()

# QUESTION AND ANSWER AREA

tk.Label(
    quiz_content,
    text="SOLVE THIS",
    font=(FONT, 11, "bold"),
    bg=PANEL,
    fg=PURPLE
).pack(pady=5)

question_label = tk.Label(
    quiz_content,
    text="5 + 5",
    font=(FONT, 36, "bold"),
    bg=PANEL,
    fg=WHITE
)
question_label.pack(pady=8)

tk.Label(
    quiz_content,
    text="YOUR ANSWER",
    font=(FONT, 10, "bold"),
    bg=PANEL,
    fg=GREY
).pack(pady=4)

answer_entry = RoundedEntry(quiz_content)
answer_entry.pack(pady=7)

# SUBMIT BUTTON AND FEEDBACK

submit_button = RoundedButton(
    quiz_content,
    text="SUBMIT ANSWER  →",
    command=check_answer,
    width=300,
    height=52,
    colour=PURPLE,
    hover_colour="#7540C4",
    font=(FONT, 14, "bold")
)
submit_button.pack(pady=8)

# Displays messages when the answer is correct or incorrect.
feedback_label = tk.Label(
    quiz_content,
    text="ENTER YOUR ANSWER BELOW",
    font=(FONT, 10, "bold"),
    bg=PANEL,
    fg=GREY
)
feedback_label.pack(pady=5)

# RESULTS SCREEN

results_frame = RoundedPanel(root, 500, 500, PANEL)
results_content = results_frame.content

tk.Label(
    results_content,
    text="CHALLENGE COMPLETE",
    font=(FONT, 21, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(pady=(35, 15))

result_grade = tk.Label(
    results_content,
    text="A",
    font=(FONT, 70, "bold"),
    bg=PANEL,
    fg=CYAN
)
result_grade.pack(pady=5)

result_score = tk.Label(
    results_content,
    text="80 / 100",
    font=(FONT, 22, "bold"),
    bg=PANEL,
    fg=WHITE
)
result_score.pack(pady=8)

result_message = tk.Label(
    results_content,
    text="EXCELLENT WORK!",
    font=(FONT, 12, "bold"),
    bg=PANEL,
    fg=PURPLE
)
result_message.pack(pady=8)

# RESULTS BUTTONS

# Allows the user to return to the menu and play another quiz.
replay_button = RoundedButton(
    results_content,
    text="PLAY AGAIN",
    command=replay_quiz,
    width=280,
    height=50,
    colour=PURPLE,
    hover_colour="#7540C4"
)
replay_button.pack(pady=12)

# Closes the application from the results screen.
exit_button = RoundedButton(
    results_content,
    text="EXIT GAME",
    command=exit_quiz,
    width=280,
    height=45,
    colour=PANEL2,
    hover_colour="#363A5B",
    text_colour=CYAN
)
exit_button.pack(pady=5)

# KEYBOARD CONTROLS

# Allows the user to submit an answer by pressing Enter.
root.bind("<Return>", lambda event: check_answer())

# RUN APPLICATION

# Displays the difficulty selection screen when the program starts.
display_menu()

root.mainloop()
