import re
import collections
from nltk.tokenize import sent_tokenize


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

    def generate(self, sentences: list) -> None:
        """
        Use a list of messages sent by the user to populate the lexicon.

        Args:
            sentences (list): List of sentences in the input text.
        """

        queue = collections.deque(maxlen=4)

        dataset = {
            "unigrams": {},
            "bigrams": {},
            "trigrams": {},
            "4-grams": {},
            "wordCount": 0,
        }

        # Loop through all sentences
        for sentence in sentences:
            # Use an empty string to mark the beggining of a new sentence
            queue.append(".")

            # Clean sentence text.
            text = re.sub(r"\s\-\s|\-\-+", " ", sentence)
            text = re.sub(r"[^\w\s\-]", " ", text)
            text = re.sub(r"\_", r"", text)

            # Split clean sentence into a list of words
            words = text.split()
            for word in words:

                # Increment word count
                dataset["wordCount"] += 1

                # Add word to queue
                queue.append(word)

                # Count word frequency
                if word not in dataset["unigrams"]:
                    dataset["unigrams"][word] = {"freq": 1}
                else:
                    dataset["unigrams"][word]["freq"] += 1

                # Count word pair frequency
                if len(queue) >= 2:
                    pair = " ".join(list(queue)[:2])
                    if pair not in dataset["bigrams"]:
                        dataset["bigrams"][pair] = {"freq": 1}
                    else:
                        dataset["bigrams"][pair]["freq"] += 1

                # Count 3 word group frequency
                if len(queue) >= 3:
                    triad = " ".join(list(queue)[:3])
                    if triad not in dataset["trigrams"]:
                        dataset["trigrams"][triad] = {"freq": 1}
                    else:
                        dataset["trigrams"][triad]["freq"] += 1

                # Count 4 word group frequency
                if len(queue) == 4:
                    group = " ".join(list(queue))
                    if group not in dataset["4-grams"]:
                        dataset["4-grams"][group] = {"freq": 1}
                    else:
                        dataset["4-grams"][group]["freq"] += 1

        dataset["unigrams"]["."] = {"freq": len(sentences)}

        # Set lexicon
        self.lexicon = dataset

        # Calculate probabilities
        self.__calculate_probabilities()
        return

    def update(self, text: str) -> None:
        """
        Update the probability of unigrams, bigrams, trigrams and 4-grams in the lexicon.

        Args:
            text (str): New text for the model to consider.
        """

        # Splitting text into a list of words
        sentences = sent_tokenize(text.lower())

        queue = collections.deque(maxlen=4)

        for sentence in sentences:
            # Use an empty string to mark the beggining of a new sentence
            queue.append(".")

            # Clean sentence text.
            text = re.sub(r"\s\-\s|\-\-+", " ", sentence)
            text = re.sub(r"[^\w\s\-]", " ", text)
            text = re.sub(r"\_", r"", text)

            # Split clean sentence into a list of words
            words = text.split()
            for word in words:

                # Increment word count
                self.lexicon["wordCount"] += 1

                # Add word to queue
                queue.append(word)

                # Count word frequency
                if word not in self.lexicon["unigrams"]:
                    self.lexicon["unigrams"][word] = {"freq": 1}
                else:
                    self.lexicon["unigrams"][word]["freq"] += 1
                prob = (
                    self.lexicon["unigrams"][word]["freq"] / self.lexicon["wordCount"]
                )
                self.lexicon["unigrams"][word]["prob"] = prob

                # Count word pair frequency
                if len(queue) >= 2:
                    pair = " ".join(list(queue)[:2])
                    if pair not in self.lexicon["bigrams"]:
                        self.lexicon["bigrams"][pair] = {"freq": 1}
                    else:
                        self.lexicon["bigrams"][pair]["freq"] += 1
                    prob = (
                        self.lexicon["bigrams"][pair]["freq"]
                        / self.lexicon["unigrams"][pair.split()[0]]["freq"]
                    )
                    self.lexicon["bigrams"][pair]["prob"] = prob

                # Count 3 word group frequency
                if len(queue) >= 3:
                    triad = " ".join(list(queue)[:3])
                    if triad not in self.lexicon["trigrams"]:
                        self.lexicon["trigrams"][triad] = {"freq": 1}
                    else:
                        self.lexicon["trigrams"][triad]["freq"] += 1
                    prob = (
                        self.lexicon["trigrams"][triad]["freq"]
                        / self.lexicon["bigrams"][" ".join(triad.split()[:2])]["freq"]
                    )
                    self.lexicon["trigrams"][triad]["prob"] = prob

                # Count 4 word group frequency
                if len(queue) == 4:
                    group = " ".join(list(queue))
                    if group not in self.lexicon["4-grams"]:
                        self.lexicon["4-grams"][group] = {"freq": 1}
                    else:
                        self.lexicon["4-grams"][group]["freq"] += 1
                    prob = (
                        self.lexicon["4-grams"][group]["freq"]
                        / self.lexicon["trigrams"][" ".join(group.split()[:3])]["freq"]
                    )
                    self.lexicon["4-grams"][group]["prob"] = prob

        return

    def __calculate_probabilities(self) -> None:
        """
        Calculate the probability of the unigrams, bigrams, trigrams and 4-grams in the lexicon.
        """

        # Calculate the probability of each unigram
        for word in self.lexicon["unigrams"]:
            prob = self.lexicon["unigrams"][word]["freq"] / self.lexicon["wordCount"]
            self.lexicon["unigrams"][word]["prob"] = prob

        # Calculate the probability of each bigram
        for pair in self.lexicon["bigrams"]:
            prob = (
                self.lexicon["bigrams"][pair]["freq"]
                / self.lexicon["unigrams"][pair.split()[0]]["freq"]
            )
            self.lexicon["bigrams"][pair]["prob"] = prob

        # Calculate the probability of each trigram
        for triad in self.lexicon["trigrams"]:
            prob = (
                self.lexicon["trigrams"][triad]["freq"]
                / self.lexicon["bigrams"][" ".join(triad.split()[:2])]["freq"]
            )
            self.lexicon["trigrams"][triad]["prob"] = prob

        # Calculate the probability of each 4-gram
        for group in self.lexicon["4-grams"]:
            prob = (
                self.lexicon["4-grams"][group]["freq"]
                / self.lexicon["trigrams"][" ".join(group.split()[:3])]["freq"]
            )
            self.lexicon["4-grams"][group]["prob"] = prob

        return