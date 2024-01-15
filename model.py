print("\nStep 0 of 10: Importing libraries and modules...")
import os
import json
import numpy
import logging

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

logger = tf.get_logger()
logger.setLevel(logging.ERROR)
from dotenv import load_dotenv
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense

load_dotenv()

# 1. Load dataset from JON file
print("\nStep 1 of 10: Loading JSON dataset")
with open(f'training_data/{os.getenv("TRAINING_DATA_SET")}', "r") as file:
    dataset = json.load(file)

# 2. Extract texts and labels from the dataset
print("\nStep 2 of 10: Extracting texts and labels from dataset")
texts = []
labels = []
for entry in dataset:
    # 2.1. Append text and terms
    texts.append(entry[os.getenv("ENTRY_TEXT_TITLE")])
    # 2.2. Append label to labels array
    label = (
        1 if entry[os.getenv("ENTRY_LABEL_TITLE")] == os.getenv("POSITIVE_LABEL") else 0
    )
    labels.append(label)

# 3. Tokenize the texts and find the total number of words in its vocabulary
print("\nStep 3 of 10: Tokenizer creation, Updating Tokenizer Vocabulary")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)

# 4. Convert texts to sequences
print("\nStep 5 of 10: Convert texts to Sequences")
sequences = tokenizer.texts_to_sequences(texts)

# 5. Pad sequences for uniform length
print("\nStep 6 of 10: Pad Sequences to uniform length for Neural Network")
padded_sequences = pad_sequences(sequences)

# 6. Define the Input and Embedding layers
# 6.1. Define an Input tensor for texts (Keras uses this to define a Input layer bts)
input_layer = Input(shape=(padded_sequences.shape[1],))
# 6.2 Define Embedding layer for word embeddings
embedding_layer = Embedding(
    input_dim=len(tokenizer.word_index) + 1,
    output_dim=100,
    input_length=padded_sequences.shape[1],
)(input_layer)
# 6.3. Define Flatten layer to flatten output of the embedding layers
flatten_layer = Flatten()(embedding_layer)
# 6.4. Define Dense layer for processing (L2 Regularizer with relatively high 0.5 strength for small dataset with approx. 100 entries)
dense_layer = Dense(units=32, activation="relu", kernel_regularizer=l2(0.5))(
    flatten_layer
)
# 6.5. Define Output layer (Dense) for binary classification
output_layer = Dense(units=1, activation="sigmoid")(dense_layer)

# 7. Create the model
print("\nStep 7 of 10: Creating and Compiling model...")
model = Model(inputs=input_layer, outputs=output_layer, name="Maven.AI")

# 8. Compile the model with updated libraries
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 9. Display model summary
print("\n\n")
model.summary()

# 10. Convert labels to numpy array
print("\nStep 8 of 10: Converting labels to numpy array")
labels = numpy.array(labels)

# 11. Train the model
print("\nStep 9 of 10: Training model...")
model.fit(padded_sequences, labels, epochs=10)

# 12. Save the tokenizer and model for later use
print("\nStep 10 of 10: Saving Tokenizers to .json and Model to .keras")
with open("saved_models/tokenizer.json", "w", encoding="utf-8") as file:
    file.write(tokenizer.to_json())

model.save("saved_models/maven_ai_model.keras")
print("\nSteps completed")
