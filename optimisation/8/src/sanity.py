import even_samples
import cifar_costf
import numpy as np
import keras

# (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
# x_train = x_train.astype("float32") / 255
# x_test = x_test.astype("float32") / 255
# num_classes = 10
# y_train = keras.utils.to_categorical(y_train, num_classes)
# y_test = keras.utils.to_categorical(y_test, num_classes)

(x_train, y_train), (x_test, y_test)= even_samples.even_sample_categories(1000)
print(cifar_costf.costf(np.array([128, 0.001, 0.9, 0.999, 40]), (x_train,y_train), (x_test,y_test)))
