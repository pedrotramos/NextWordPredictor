import json
from .lexicon import Lexicon


def setup():
    # Hardcoded parameters
    INPUT_FILE = "dom_casmurro.txt"  # Dataset file name

    # Creating the lexicon
    lex = Lexicon()
    lex.populate(INPUT_FILE)

    # Writing the dataset file
    with open("dataset.json", "w", encoding="UTF-8") as file:
        json.dump(lex.lexicon, fp=file, indent=4)