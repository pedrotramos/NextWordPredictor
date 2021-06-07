import re
import json
from pathlib import Path
from modules.setup import setup
from modules.lexicon import Lexicon
from modules.predictor import predict

if __name__ == "__main__":

    # Check if dataset exists
    dataset = Path("dataset.json")
    if not dataset.exists():
        # Do the setup if it doesn't already exist
        setup()

    # Read the dataset
    with dataset.open() as file:
        data = json.load(file)

    # Setting up the lexicon object
    lex = Lexicon()
    lex.get_lexicon(data)

    # Getting an input from the user
    user_input = input("> ")

    # Cleaning user input
    text = re.sub(r"\s\-\s|\-\-+", " ", user_input)
    text = re.sub(r"[^\w\s\-]", " ", text)
    text = re.sub(r"\_", r"", text)

    # Splitting the normalized input into words
    words = text.lower().split()

    # Predict the next word based on the user's input.
    if len(words) > 0:
        prediction = predict(words, data)
        # Print the 3 predicted options
        for i, pred in enumerate(prediction):
            print(f"{i + 1}. {pred[0]}")
        # Updating the lexicon
        lex.update(text)
        # Saving the updated lexicon
        with open("dataset.json", "w", encoding="UTF-8") as file:
            json.dump(lex.lexicon, fp=file, indent=4)
    else:
        print("Não é possível prever a próxima palavra de uma entrada vazia.")
