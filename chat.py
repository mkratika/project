import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.tokenize import WhitespaceTokenizer
import keras
from keras import backend
import tensorflow as tf
from tensorflow import keras
import random
import json
import numpy
import pickle

#%%
with open("files.json") as file:
    data = json.load(file)

try:
    with open("data.pickle" , "rb") as f:
        words, labels, training ,output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["files"]:
        for pattern in intent["patterns"]:
            wrds = WhitespaceTokenizer().tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []
    out_empty = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)
    with open("data.pickle" , "wb") as f:
        pickle.dump((words, labels, training ,output), f)
#%%
def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    s_words = WhitespaceTokenizer().tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)
#%%
def chat():
    print("Start talking to the bot (Type 'quit' to exit)")
    while True:
        inp = input("You : ")
        if inp.lower() == "quit":
            break
        inp_bag = bag_of_words(inp, words)
        inp_bag = numpy.array([inp_bag])  # Reshape the input to match the model's expected input shape
        result = model.predict(inp_bag)[0]
        result_index = numpy.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.6:
            for tg in data["files"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]

            print(random.choice(responses))
        else:
            print("I am Sorry, I did not get that")
#%%
keras.backend.clear_session()
inputs = tf.keras.layers.Input(shape = (len(training[0]),))
x = tf.keras.layers.Reshape((1, len(training[0])))(inputs)
net = tf.keras.layers.Dense(10, activation='relu')(x)
net = tf.keras.layers.Dense(10, activation='relu')(net)
net = tf.keras.layers.Flatten()(net)
outputs = tf.keras.layers.Dense(len(output[0]), activation='softmax')(net)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

try:
    model.load("model.keras")
except:
    model.fit(training, output, epochs=2000, batch_size = 10, verbose = 1)
    model.save("model.keras")

chat()