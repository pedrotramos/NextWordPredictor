import re


class Lexicon:
    def __init__(self) -> None:
        self.lexicon = dict()

    def get_lexicon(self, data: dict) -> None:
        """
        Get a lexicon previously populated.

        Args:
            data (dict): Dictionary object containing a previous state of the model.
        """
        self.lexicon = data

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
        if currentWord not in self.lexicon:
            self.lexicon[currentWord] = {nextWord: {"freq": 1}}
            self.lexicon[currentWord][nextWord]["prob"] = 1
            return

        else:
            # Get all the next word options.
            nextWordOptions = self.lexicon[currentWord]

            # Check if the output word is among the next word options.
            if nextWord in nextWordOptions:
                nextWordOptions[nextWord]["freq"] += 1
            else:
                nextWordOptions[nextWord] = {"freq": 1}
                nextWordOptions[nextWord]["prob"] = None

            self.lexicon[currentWord] = nextWordOptions
            self.__calculate_probabilities(currentWord)
            return

    def update(self, sentence: str) -> None:
        """
        Update the probability of each next word option.

        Args:
            sentence (str): New sentence for the model to consider.
        """

        # Clean input text.
        text = re.sub(r"\s\-\s|\-\-+", " ", sentence)
        text = re.sub(r"[^\w\s\-]", " ", text)
        text = re.sub(r"\_", r"", text)

        # Splitting clean text into a list of words
        words = sentence.lower().split()

        # Update values for every word in the sentence
        for i in range(len(words) - 1):
            currentWord = words[i]
            nextWord = words[i + 1]
            # Add the input word to the lexicon when it isn't in there yet.
            if currentWord not in self.lexicon:
                self.lexicon[currentWord] = {nextWord: {"freq": 1}}
                self.lexicon[currentWord][nextWord]["prob"] = 1

            else:
                # Get all the next word options.
                nextWordOptions = self.lexicon[currentWord]

                # Check if the output word is among the next word options.
                if nextWord in nextWordOptions:
                    nextWordOptions[nextWord]["freq"] += 1
                else:
                    nextWordOptions[nextWord] = {"freq": 1}
                    nextWordOptions[nextWord]["prob"] = None

                self.lexicon[currentWord] = nextWordOptions
                self.__calculate_probabilities(currentWord)
        return

    def __calculate_probabilities(self, word: str) -> None:
        """
        Calculate the probability of each next word option.

        Args:
            word (str): Word to have its next word options probabilities calculated.
        """
        # Get the all of the next word options.
        nextWords = self.lexicon[word]

        sumOfFreqs = sum(w["freq"] for w in nextWords.values() if w)

        # Calculate the probability of each next word option.
        for w in nextWords.keys():
            nextWords[w]["prob"] = nextWords[w]["freq"] / sumOfFreqs

        # Save probabilities to lexicon
        self.lexicon[word] = nextWords
        return