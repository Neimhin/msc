import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description='Plot training history from CSV file.')
    parser.add_argument('--history-csv', type=str, required=True, help='Path to the CSV file containing training history.')
    parser.add_argument('--fig', type=str, required=True, help='Filename for the saved figure.')
    return parser.parse_args()

def plot_history(history_csv, figfile):
    history = pd.read_csv(history_csv)

    plt.figure(figsize=(12, 12))

    # accuracy subplot
    plt.subplot(211)
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    # loss subplot
    plt.subplot(212)
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.savefig(figfile)

if __name__ == "__main__":
    args = parse_args()
    plot_history(args.history_csv, args.fig)
