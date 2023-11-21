import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.size'] = 18

data = pd.read_csv('fig/size-v-accuracy.csv')
train_data = data[data['dataset'] == 'train'].sort_values(by="training-samples")
test_data = data[data['dataset'] == 'test'].sort_values(by="training-samples")
plt.figure(figsize=(6, 6))
plt.plot(train_data['training-samples'], train_data['accuracy'], label='Training Accuracy', color='blue', marker='o')
plt.plot(test_data['training-samples'], test_data['accuracy'], label='Test Accuracy', color='red', marker='o')

plt.title('Model Accuracy vs. Training Samples')
plt.xlabel('Number of Training Samples')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('fig/size-v-accuracy.pdf')

