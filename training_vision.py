from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from keras import callbacks
import os
import mediapipe as mp
import cv2
import numpy as np

DATA_PATH = os.path.join('MP_Data') 
sequence_length = 15

# f = open("action.txt",'r')
# temp = f.readlines()
# temp = [s.replace("\n","") for s in temp]
# temp = [s.replace(" ","") for s in temp]
# actions = np.array(temp)

actions = np.array(['A','free','B','C'])

label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])
X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(15,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
es = callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=200, restore_best_weights=True)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=2000,batch_size=450 ,verbose=1, callbacks=[es])
model.save("action.keras")


res = model.predict(X_test)
# print(np.sum(res))
print(actions[np.argmax(res[0])])
print(actions[np.argmax(y_test[0])])

print(" ")

print(actions[np.argmax(res[1])])
print(actions[np.argmax(y_test[1])])

print(" ")


print(actions[np.argmax(res[2])])
print(actions[np.argmax(y_test[2])])

print(" ")


print(actions[np.argmax(res[3])])
print(actions[np.argmax(y_test[3])])

print(" ")


print(actions[np.argmax(res[4])])
print(actions[np.argmax(y_test[4])])

model.summary()