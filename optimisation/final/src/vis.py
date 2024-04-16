import pandas as pd
import lib
import matplotlib.pyplot as plt

ap = lib.default_args()
ap.add_argument('--step-history-csv', type=str, required=True)
args = ap.parse_args()

df = pd.read_csv(args.step_history_csv)


plt.figure(figsize=(12, 6))

# categorical cross-entropy loss
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
plt.plot(df['step'], df['train_loss'], label='train', color='blue')
plt.plot(df['step'], df['val_loss'], label='val', color='red')
plt.yscale('log')
plt.title('Loss')
plt.xlabel('Step')
plt.ylabel('Log Loss')
plt.legend()

# accuracy
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
plt.plot(df['step'], df['train_accuracy'], label='train', color='blue')
plt.plot(df['step'], df['val_accuracy'], label='val', color='red')
plt.title('Accuracy')
plt.xlabel('Step')
plt.ylabel('Accuracy')
plt.ylim([0, 1])  # Set y-axis limits to [0, 1]
plt.legend()

plt.legend()
plt.show()
