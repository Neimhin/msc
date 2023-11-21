import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.size'] = 18

data = pd.read_csv('fig/l1-v-accuracy.csv')
train_data = data[data['dataset'] == 'train'].sort_values(by="l1")
test_data = data[data['dataset'] == 'test'].sort_values(by="l1")
plt.figure(figsize=(6, 6))
plt.plot(train_data['l1'], train_data['accuracy'], label='Training Accuracy', color='blue', marker='o')
plt.plot(test_data['l1'], test_data['accuracy'], label='Test Accuracy', color='red', marker='o')

plt.title('Model Accuracy vs. $L_1$')
plt.xlabel('$L_1$')
plt.xscale("log")
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('fig/l1-v-accuracy.pdf')

