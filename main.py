# Import necessary libraries
import random
from tkinter import *
import pandas as pd
from random import choice

# Define constants
BACKGROUND_COLOR = "#B1DDC6"  # Background color for the application
current_card = {}  # Initialize an empty dictionary for the current flashcard
french_word = {}  # Initialize an empty dictionary for French words
try:
    # Try to read the known French words data from a CSV file
    df = pd.read_csv("data/known_french_words.csv")
except FileNotFoundError:
    # If the file doesn't exist, read the original French words data
    original_data = pd.read_csv("data/french_words.csv")
    french_word = original_data.to_dict(orient="records")
else:
    # If the known words data was successfully loaded, store it in french_word
    french_word = df.to_dict(orient="records")

# Function to handle the case when time is over
def time_over():
    # Update the card to display the English word
    canvas.itemconfig(french_or_english, fill="white", text="English")
    canvas.itemconfig(french_word_place, fill="white", text=current_card['English'])
    canvas.itemconfig(card_img, image=card_back)

# Function to move to the next flashcard
def move_next():
    global current_card, after_trigger
    # Cancel the scheduled time_over function
    window.after_cancel(after_trigger)
    # Select a new random flashcard
    current_card = choice(french_word)
    # Update the card to display the French word
    canvas.itemconfig(french_or_english, text="French", fill="black")
    canvas.itemconfig(french_word_place, text=current_card['French'], fill="black")
    canvas.itemconfig(card_img, image=card_front)
    # Schedule time_over function to trigger in 3000 milliseconds (3 seconds)
    after_trigger = window.after(3000, func=time_over)

# Function to handle known words
def known_words():
    # Remove the current flashcard from the list of French words
    french_word.remove(current_card)
    # Convert the updated list to a DataFrame
    data = pd.DataFrame(french_word)
    # Save the updated data to a CSV file for known words
    data.to_csv("data/known_french_words.csv", index=False)
    # Move to the next flashcard
    move_next()

# Create the main application window
window = Tk()
window.title("Flashy")
window.config(padx=50, background=BACKGROUND_COLOR, pady=50)

# Schedule the initial time_over function to trigger in 3000 milliseconds
after_trigger = window.after(3000, func=time_over)

# Create a canvas to display flashcards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 265, image=card_front)
french_or_english = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
french_word_place = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(column=1, row=0, columnspan=2)

# Start by displaying the first flashcard
move_next()

# Create a button to handle wrong answers
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=move_next)
wrong_button.grid(column=1, row=1)

# Create a button to handle correct answers (known words)
right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=known_words)
right_button.grid(column=2, row=1)

# Start the main event loop for the application
window.mainloop()
