import json
import pickle
from tensorflow.keras.models import load_model 
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


with open ("intents.json") as file:
    data = json.load(file)\
    
with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)
model = load_model("chat_model.h5")

while True:
    input_text = input("Enter your command->")
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=20, truncating='post')
    result = model.predict(padded_sequences)
    tag = label_encoder.inverse_transform([np.argmax(result)])[0]

    for i in data['intents']:
        if i['tag'] == tag:
            print(np.random.choice(i['responses']))


