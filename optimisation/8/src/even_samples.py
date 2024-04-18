import numpy as np
import keras 
from sklearn.model_selection import StratifiedShuffleSplit

num_classes = 10

def even_sample_categories(n):
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (x_train[1:n], y_train[1:n]), (x_test, y_test)

if __name__ == "__main__":
    # Example usage
    X_train_even, y_train_even = even_sample_categories(num_samples_per_class=10)
    print(X_train_even, y_train_even)
    print(x_train.shape, y_train.shape)
    print(X_train_even.shape, y_train_even.shape)
