
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import shuffle
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
    parser.add_argument('--l1-reg', type=float, default=0.001,
                        help='L1 regularization weight.')
    parser.add_argument('--max-pool', action='store_true',
                        help='Use max-pooling instead of stride.')
    
    return parser.parse_args()

args = parse_args()

import keras
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
y_train = y_train.flatten()
y_test = y_test.flatten()
clf = DummyClassifier(strategy="most_frequent")
clf.fit(x_train[:5000], y_train[:5000])

# Make predictions on the test set
y_pred = clf.predict(x_test)

# Calculate and print metrics
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
