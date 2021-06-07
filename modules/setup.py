import json
from .lexicon import Lexicon
from .extractFromWpp import Extractor


def setup():
    USER_NAME = input("Enter your Whatsapp name: ")

    extractor = Extractor(USER_NAME)
    messages = extractor.extract()

    # Creating the lexicon
    lex = Lexicon()
    lex.generate(messages)

    # Writing the dataset file
    with open("dataset.json", "w", encoding="UTF-8") as file:
        json.dump(lex.lexicon, fp=file, indent=4)