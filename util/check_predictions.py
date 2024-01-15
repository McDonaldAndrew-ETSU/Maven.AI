import os
from dotenv import load_dotenv
from util.json_logger import (
    false_positive_logger,
    false_negative_logger,
    true_positive_logger,
    true_negative_logger,
)

load_dotenv()


def check_predictions(predictions, input_data_array):
    """
    Estimates if prediction was correct or not. If not, the function determines
    if it was a false positive or false negative and logs it to its associated file
    """
    keywords = os.getenv("KEYWORDS").split(",")
    for index, text in enumerate(input_data_array):
        matching = [keyword for keyword in keywords if keyword in text]

        new_prediction = predictions[index]
        new_prediction += len(matching) * 0.01 if matching else -len(keywords) * 0.02

        if predictions[index] >= 0.5 and new_prediction <= 0.5:
            # False Positive
            false_positive_logger.log(predictions[index], text)
        elif predictions[index] <= 0.5 and new_prediction >= 0.5:
            # False Negative
            false_negative_logger.log(predictions[index], text)
        elif predictions[index] >= 0.5 and new_prediction >= 0.5:
            # True Positive
            true_positive_logger.log(predictions[index], text)
        elif predictions[index] <= 0.5 and new_prediction <= 0.5:
            # True Negative
            true_negative_logger.log(predictions[index], text)

    return
