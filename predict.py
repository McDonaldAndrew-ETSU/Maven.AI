print("\nImporting libraries and modules...")
import os
import json
import logging

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

logger = tf.get_logger()
logger.setLevel(logging.ERROR)
from dotenv import load_dotenv
from util.clear_terminal import clear_terminal
from tensorflow.keras.models import load_model
from util.check_predictions import check_predictions
from util.data_file_to_dict import data_file_to_dict
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

load_dotenv()

# 1. Load the tokenizer
print("\nLoading tokenizers from json files...")
with open("saved_models/tokenizer.json", "r", encoding="utf-8") as file:
    tokenizer = tokenizer_from_json(file.read())
# 2. Load the trained model
print("\nLoading trained model...")
model = load_model("saved_models/applyer_ai_model.keras")
clear_terminal()


# 3. Function to preprocess input text  and make predictions
def predict_decision(input_data: dict):
    # 3.1. Get the input shape from the first model (since there are two Input layers of the same shape )
    input_shape = model.input_shape[1]

    # 3.2. Turn the input texts into an array and sequence them
    sequences = tokenizer.texts_to_sequences(input_data)

    # 3.3. Pad the sequences and set the max length to the input
    padded_sequences = pad_sequences(sequences, maxlen=input_shape)

    # 3.2. Make a prediction
    predictions = model.predict(padded_sequences, verbose=0)

    check_predictions(predictions, input_data)

    return


# Example usage
input_titles = data_file_to_dict("test_data/data.txt")
predict_decision(input_titles)
