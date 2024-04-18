import pandas as pd
import numpy as np
import tensorflow as tf
import os
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from keras.optimizers import SGD
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, LeakyReLU
from keras.callbacks import Callback
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import argparse 
import sgd

step_history = {
        'train_loss': [],
        'val_loss': [],
        'batch_loss': [],
        'train_accuracy': [],
        'val_accuracy': [],
        'batch_accuracy': [],
        'step': [],
        'epoch': [],
}

step_number = 0

class StepMetricsCallback(Callback):
    def on_epoch_begin(self, i, logs=None):
        self.current_epoch = i

    def on_train_batch_end(self, i, logs=None):
        global x_train, y_train, x_val, y_val, step_number, optimizer
        train_loss, train_accuracy = self.model.evaluate(x_train, y_train)
        val_loss, val_accuracy = self.model.evaluate(x_val, y_val)
        step_history['train_loss'].append(train_loss)
        step_history['val_loss'].append(val_loss)
        step_history['batch_loss'].append(logs['loss'])
        step_history['train_accuracy'].append(train_accuracy)
        step_history['val_accuracy'].append(val_accuracy)
        step_history['batch_accuracy'].append(logs['accuracy'])
        step_history['step'].append(step_number)
        step_history['epoch'].append(self.current_epoch)
        step_number += 1
        pd.DataFrame(step_history).to_csv(exp + f"/step-history-{step_number}.csv")

ap = argparse.ArgumentParser()
ap.add_argument("--batch-size", type=int, default=128)
ap.add_argument("--run-name", type=str, required=True)
ap.add_argument("--dropout", type=float, default=0.1)
ap.add_argument("--fold", type=int, default=0)
ap.add_argument("--show", type=bool, default=False)
args = ap.parse_args()

exp = f"exp-step/{args.batch_size}/{args.run_name}"


plt.rc('font', size=18)
plt.rcParams['figure.constrained_layout.use'] = True
import sys

# Model / data parameters
num_classes = 10
input_shape = (32, 32, 3)

# the data, split between train and test sets
train, test = keras.datasets.cifar10.load_data()
n=4096
# x_train = train[0][:n]; y_train=train[1][:n]
# x_val   = train[0][n:n+512]; y_val = train[1][n:n+512]
# x_train_eval = x_train[:512]; y_train_eval = y_train[:512]

kf = KFold(n_splits=9, shuffle=True, random_state=42)

train_val_indices = list(kf.split(train[0][:n+512]))[args.fold]
traini, vali = train_val_indices

x_train = train[0][traini]; y_train=train[1][traini]
x_val   = train[0][vali]; y_val = train[1][vali]

print(x_train.shape, y_train.shape)
print(x_val.shape, y_val.shape)
print(x_val.mean())
#x_test=x_test[1:500]; y_test=y_test[1:500]

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_val = x_val.astype("float32") / 255
test_slice = slice(None, None, None)
x_test = test[0][test_slice].astype("float32") / 255
print("orig x_train shape:", x_train.shape)

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
# y_train_eval = keras.utils.to_categorical(y_train_eval, num_classes)
y_test = keras.utils.to_categorical(test[1][test_slice], num_classes)
y_val = keras.utils.to_categorical(y_val, num_classes)

model = keras.Sequential()
model.add(Conv2D(16, (3,3), padding='same', input_shape=x_train.shape[1:],activation='relu'))
model.add(Conv2D(16, (3,3), strides=(2,2), padding='same', activation='relu'))
model.add(Conv2D(32, (3,3), padding='same', activation='relu'))
model.add(Conv2D(32, (3,3), strides=(2,2), padding='same', activation='relu'))
model.add(Dropout(args.dropout))
model.add(Flatten())
model.add(Dense(num_classes, activation='softmax')) #,kernel_regularizer=regularizers.l1(0.0001)))
# optimizer = sgd.SGD(learning_rate=0.01)
optimizer = SGD(learning_rate=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
model.summary()

batch_size = args.batch_size
steps_per_epoch  = n / batch_size
epochs = max(2, int(4096 / steps_per_epoch))
print(epochs, steps_per_epoch, batch_size, n)
os.makedirs(exp)
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_val, y_val), callbacks=[StepMetricsCallback()])

model.save(exp+"/model.tf")
pd.DataFrame(step_history).to_csv(exp + "/step-history.csv")
pd.DataFrame(history.history).to_csv(exp + "/history.csv")
plt.subplot(211)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.subplot(212)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss'); plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.savefig(exp+"/val-train.pdf")
if args.show:
    plt.show()

preds = model.predict(x_train)
y_pred = np.argmax(preds, axis=1)
y_train1 = np.argmax(y_train, axis=1)
cls_report = classification_report(y_train1, y_pred, output_dict=True)
print(cls_report)
pd.DataFrame(cls_report).to_csv(exp+"/train.cls.report.csv")
confusion = confusion_matrix(y_train1,y_pred) 
pd.DataFrame(confusion).to_csv(exp+"/train.confusion.csv")
print(confusion)

preds = model.predict(x_test)
y_pred = np.argmax(preds, axis=1)
y_test1 = np.argmax(y_test, axis=1)
cls_report = classification_report(y_test1, y_pred, output_dict=True)
pd.DataFrame(cls_report).to_csv(exp+"/test.cls.report.csv")
confusion = confusion_matrix(y_test1,y_pred) 
pd.DataFrame(confusion).to_csv(exp+"/test.confusion.csv")
