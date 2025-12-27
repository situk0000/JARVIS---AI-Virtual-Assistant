import json
import pickle
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# Step 1: Load intents.json
with open("intents.json") as file:
    data = json.load(file)

print("Data loaded successfully ✅")

# Step 2: Initialize lists
training_sentences = []
training_labels = []
labels = []
responses = []

# Step 3: Collect training data
for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

# Step 4: Encode labels
label_encoder = LabelEncoder()
label_encoder.fit(training_labels)
training_labels = label_encoder.transform(training_labels)

number_of_classes = len(labels)
print("Number of classes:", number_of_classes)

# Step 5: Tokenization and Padding
vocab_size = 1000
oov_token = "<OOV>"
max_len = 20
embedding_dim = 16

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

# Step 6: Build Model
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(number_of_classes, activation="softmax"))

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

model.summary()

# Step 7: Train Model
history = model.fit(padded_sequences,
                    np.array(training_labels),
                    epochs=1000,  # you can reduce if 1000 is too much
                    verbose=1)

# Step 8: Save Model and Objects
model.save("chat_model.h5")
print("Model saved as chat_model.h5 ✅")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

with open("label_encoder.pkl", "wb") as encoder_file:
    pickle.dump(label_encoder, encoder_file, protocol=pickle.HIGHEST_PROTOCOL)

print("Tokenizer and LabelEncoder saved ✅")
