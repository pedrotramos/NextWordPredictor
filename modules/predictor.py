import numpy as np


def predict(word: str, dataset: dict) -> list:
    """
    Get the top 3 options for next word based on the last word.

    Args:
        word (str): Last word of the input.
        dataset (dict): A dictionary containing the whole dataset.

    Returns:
        A list with the top 3 next word candidates.
    """
    if word not in dataset:
        options = list(dataset.keys())
        predictions = []
        for i in range(3):
            predicted = np.random.choice(options)
            predictions.append(predicted)
    else:
        options = dataset[word]
        best3 = sorted(options, reverse=True, key=lambda x: (options[x]["prob"]))[:3]
        predictions = [pred for pred in best3]
    return predictions
