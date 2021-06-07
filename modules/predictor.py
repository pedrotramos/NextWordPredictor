from nltk import data
import numpy as np


def get_prob_unigram(unigram: str, dataset: dict) -> float:
    """
    Get the probability of a unigram

    Args:
    unigram (str): The unigram to have its probability found.
    dataset (dict): A dictionary containing the whole dataset.
    """
    if unigram not in dataset["unigrams"]:
        return 0.0
    else:
        return dataset["unigrams"][unigram]["prob"]


def get_prob_bigram(bigram: tuple, dataset: dict) -> float:
    """
    Get the probability of a bigram

    Args:
    bigram (tuple): The bigram to have its probability found.
    dataset (dict): A dictionary containing the whole dataset.
    """
    if bigram not in dataset["bigrams"]:
        return 0.0
    else:
        return dataset["bigrams"][bigram]["prob"]


def get_prob_trigram(trigram: tuple, dataset: dict) -> float:
    """
    Get the probability of a trigram

    Args:
    trigram (tuple): The trigram to have its probability found.
    dataset (dict): A dictionary containing the whole dataset.
    """
    if trigram not in dataset["trigrams"]:
        return 0.0
    else:
        return dataset["trigrams"][trigram]["prob"]


def get_prob_4gram(fourGram: tuple, dataset: dict) -> float:
    """
    Get the probability of a fourGram

    Args:
    fourGram (tuple): The fourGram to have its probability found.
    dataset (dict): A dictionary containing the whole dataset.
    """
    if fourGram not in dataset["4-grams"]:
        return 0.0
    else:
        return dataset["4-grams"][fourGram]["prob"]


def predict(user_input: list, dataset: dict) -> list:
    """
    Get the top 3 options for next word based on the user's input.

    Args:
        user_input (list): List of words based on user's splitted input.
        dataset (dict): A dictionary containing the whole dataset.

    Returns:
        A list with the top 3 next word candidates.
    """
    predictions = []

    # Loop through all words and check for the probability if we were to generate this word
    for word in dataset["unigrams"].keys():
        p1 = get_prob_unigram(word, dataset)
        p2 = get_prob_bigram(user_input[-1] + " " + word, dataset)
        p3 = (
            get_prob_trigram(" ".join(user_input[-2:]) + " " + word, dataset)
            if len(user_input) >= 3
            else 0
        )
        p4 = (
            get_prob_4gram(" ".join(user_input[-3:]) + " " + word, dataset)
            if len(user_input) >= 4
            else 0
        )

        # Calculate probability using linear interpolation
        p = 0.5 * p4 + 0.3 * p3 + 0.15 * p2 + 0.05 * p1

        predictions.append((word, p))

    # sort based on the score and select the best one
    predictions.sort(key=lambda x: x[1], reverse=True)
    output = []
    # Check for useless prediction
    for pred in predictions[0:4]:
        if pred[0] != ".":
            output.append(pred[0])

    return output[0:3]
