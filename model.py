import re
import numpy as np


class Lexicon:
    def __init__(self) -> None:
        self.frequencies = {}
        self.lexicon = {}

    def populate(self, dataset_path: str) -> None:
        """
        Use a dataset to populate the lexicon.

        Args:
            dataset_path (str): path to the dataset file.
        """
        with open(dataset_path, "r", encoding="UTF-8") as dataset:
            text = dataset.read().lower()

        # Clean input text.
        text = re.sub(r"\s\-\s|\-\-+", " ", text)
        text = re.sub(r"[^\w\s\-]", " ", text)
        text = re.sub(r"\_", r"", text)

        # Split the text into a list of words.
        words = text.split()

        # Generate the lexicon based on the input dataset.
        for i in range(len(words) - 1):
            self.generate(words[i], words[i + 1])
        return

    def generate(self, currentWord: str, nextWord: str) -> None:
        """
        Add item to the lexicon.

        Args:
            currentWord (str): Input word.
            nextWord (str): Output word.
        """

        # Add the input word to the lexicon when it isn't in there yet.
        if currentWord not in self.frequencies:
            self.frequencies[currentWord] = {nextWord: 1}
            self.lexicon[currentWord] = {nextWord: 1}
            return

        else:
            # Get the frequencies of all the next word options.
            nextWordOptions = self.frequencies[currentWord]

            # Check if the output word is among the next word options.
            if nextWord in nextWordOptions:
                nextWordOptions[nextWord] += 1
            else:
                nextWordOptions[nextWord] = 1

            self.frequencies[currentWord] = nextWordOptions
            self.__calculate_probabilities(currentWord)
            return

    def predict(self, word: str) -> list:
        """
        Get the top 3 options for next word based on the last word.

        Args:
            word (str): Last word of the input.

        Returns:
            A list with the top 3 next word candidates.
        """
        if word not in self.lexicon:
            options = list(self.lexicon.keys())
            predictions = []
            for i in range(3):
                predicted = np.random.choice(options)
                predictions.append(predicted)
        else:
            options = self.lexicon[word]
            best3 = sorted(options)[:3]
            predictions = [pred[0] for pred in best3]
        return predictions

    def __calculate_probabilities(self, word: str) -> None:
        """
        Calculate the probability of each next word option.

        Args:
            word (str): Word to have its next word options probabilities calculated.
        """
        # Get the frequencies of the next word options.
        nextWordFrequencies = self.frequencies[word]

        # Calculate the probability of each next word option.
        probabilities = {
            (key, value / sum(nextWordFrequencies.values()))
            for key, value in nextWordFrequencies.items()
        }

        # Save probabilities to lexicon
        self.lexicon[word] = probabilities
        return


if __name__ == "__main__":

    # Hardcoded parameters
    INPUT_FILE = "dom_casmurro.txt"  # Dataset file name

    # Creating the lexicon
    lexicon = Lexicon()
    lexicon.populate(INPUT_FILE)

    # Getting an input from the user
    user_input = input("> ")

    # Splitting the normalized input into words
    words = user_input.lower().split()

    # Predict the next word using a maximum of NUM_WORDS words.
    if len(words) > 0:
        prediction = lexicon.predict(words[-1])
    else:
        print("Não é possível prever a próxima palavra de uma entrada vazia.")

    # Print the 3 predicted options
    for i, pred in enumerate(prediction):
        print(f"{i + 1}. {pred}")
