from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
to_learn = {}

# ---------------------------- ACCESS DATA --------------------------------- #
try:
    current_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = current_data.to_dict(orient="records")
# ^ using records is To get all the words/translation rows out as a list of dictionaries
# e.g. [{french_word: english_word}, {french_word2: english_word2}
# so we can get a random word. Instead of words_dict= {row.Spanish: row.English for (index, row) in df_data.iterrows()}
# print(words_dict)


def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    chosen_word = current_word["Spanish"]
    # print(chosen_word)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=chosen_word, fill="black")
    canvas.itemconfig(card_background, image=front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    meaning_word = current_word["English"]
    # print(meaning_word)
    canvas.itemconfig(card_background, image=back_img)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=meaning_word)

def is_known():
    to_learn.remove(current_word)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# -------------------------------- UI SETUP ---------------------------------- #
window = Tk()
window.title("FLASHY")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
known_button = Button(image=right_img, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()


window.mainloop()