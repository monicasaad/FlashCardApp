# required imports
from tkinter import *
import pandas
import random

# global variables
BACKGROUND_COLOR = "#B1DDC6"
chosen_word = {}

try:
    # read in data
    df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("./data/french_words.csv")
finally:
    words_to_learn = df.to_dict(orient="records")


# function that chooses a random word
def choose_word():
    global chosen_word, flip_timer
    window.after_cancel(flip_timer)
    chosen_word = random.choice(words_to_learn)
    french_word = chosen_word.get("French")
    canvas.itemconfig(flashcard, image=flashcard_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    flip_timer = window.after(3000, func=flip_card)


# function that flips flashcard
def flip_card():
    english_word = chosen_word.get("English")
    canvas.itemconfig(flashcard, image=flashcard_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")


def is_known():
    words_to_learn.remove(chosen_word)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    choose_word()

# ################### UI SETUP #######################

# create screen window
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, func=flip_card)

# canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)  # size, background colour, remove canvas outline

flashcard_front = PhotoImage(file="./images/card_front.png")
flashcard_back = PhotoImage(file="./images/card_back.png")
flashcard = canvas.create_image(400, 263, image=flashcard_front)

title_text = canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 40, "italic"))  # x pos, y pos, text
word_text = canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)

# buttons
x_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=x_img, highlightthickness=0, command=choose_word)
wrong_button.grid(row=1, column=0)

checkmark_img = PhotoImage(file="./images/right.png")
right_button = Button(image=checkmark_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

# choose first word
choose_word()


# keep screen popup open
window.mainloop()
