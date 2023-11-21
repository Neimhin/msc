
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, LeakyReLU
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import pandas as pd
plt.rc('font', size=18)
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams["text.usetex"] = True
import sys

figfile = sys.argv[1] if len(sys.argv) >= 2 else "fig/default-output.pdf"

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Argument parser for train size.')
    parser.add_argument('--train-size', type=int, choices=range(1, 50001),
                        help='Size of the training set. Must be an integer between 1 and 50000.')
    parser.add_argument('--output-history-csv', type=str,
                        help='Output filename for the history csv.')
    parser.add_argument('--output-evaluation-csv', type=str,
                        help='Output filename for the history csv.')
    parser.add_argument('--save-model-to', type=str,
                        help='Output file/folder name for the saved model.')
    parser.add_argument('--save-fit-time', type=str,
                        help='Output filename for the fit time measurement')
    parser.add_argument('--l1-reg', type=float, default=0.0001,
                        help='L1 regularization weight.')
    parser.add_argument('--max-pool', action='store_true',
                        help='Use max-pooling instead of stride.')
    parser.add_argument('--evaluation-file', type=str, default="evaluation-file.txt",
                        help='Where to store evalutions')
    parser.add_argument('--extra-layers', action="store_true",
                        help='Use two extra ConvNet layers')
    parser.add_argument('--epochs', default=20,type=int,
                        help='Use two extra ConvNet layers')
    
    return parser.parse_args()

args = parse_args()

# Model / data parameters
num_classes = 10
input_shape = (32, 32, 3)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
n=args.train_size
x_train = x_train[1:n]; y_train=y_train[1:n]
#x_test=x_test[1:500]; y_test=y_test[1:500]

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
print("orig x_train shape:", x_train.shape)

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


def mk_model():
    global args
    model = None
    model = keras.Sequential()
    model.add(keras.Input(shape=x_train.shape[1:]))
    if not args.max_pool:
        if args.extra_layers:
            model.add(Conv2D(8, (3,3), padding='same',activation='relu'))
            model.add(Conv2D(8, (3,3), strides=(2,2), padding='same', activation='relu'))

        model.add(Conv2D(16, (3,3), padding='same',activation='relu'))
        model.add(Conv2D(16, (3,3), strides=(2,2), padding='same', activation='relu'))
        model.add(Conv2D(32, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(32, (3,3), strides=(2,2), padding='same', activation='relu'))
        model.add(Dropout(0.5))
        model.add(Flatten())
        model.add(Dense(num_classes, activation='softmax',kernel_regularizer=regularizers.l1(args.l1_reg)))
        model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["accuracy"])
        model.summary()
    else:
        model.add(Conv2D(16, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(16, (3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(32, (3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Dropout(0.5))
        model.add(Flatten())
        model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l1(args.l1_reg)))
        model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["accuracy"])
        model.summary()
    return model


batch_size = 128
epochs = args.epochs
model = mk_model()
def fit_and_save_timing():
    import time
    global args, model
    start_time = time.time()
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
    end_time = time.time()
    timing_str = f"{args.train_size},{end_time - start_time}\n"
    print(timing_str)
    if args.save_fit_time:
        with open(args.save_fit_time, "w") as f:
            f.write(timing_str)
    return history
history = fit_and_save_timing()
if args.save_model_to:
    model.save(args.save_model_to)
if args.output_history_csv:
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(args.output_history_csv)

with open(args.evaluation_file, 'w') as f:
    def p(*args,**kwargs):
        print(*args,file=f,**kwargs)
    preds = model.predict(x_train)
    y_pred = np.argmax(preds, axis=1)
    y_train1 = np.argmax(y_train, axis=1)
    p("train:")
    p(classification_report(y_train1, y_pred))
    p(confusion_matrix(y_train1,y_pred))

    preds = model.predict(x_test)
    y_pred = np.argmax(preds, axis=1)
    y_test1 = np.argmax(y_test, axis=1)
    p("\n\ntest:")
    p(classification_report(y_test1, y_pred))
    p(confusion_matrix(y_test1,y_pred))
