import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.size'] = 18

def parse_args():
    parser = argparse.ArgumentParser(description='Plot training history from CSV file.')
    parser.add_argument('--history-csv', type=str, required=True, help='Path to the CSV file containing training history.')
    parser.add_argument('--fig', type=str, required=True, help='Filename for the saved figure.')
    parser.add_argument('--suptitle', type=str, required=True, help='Suptitle for the plot.')
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
    # plt.ylim((0.2,0.8))

    # loss subplot
    plt.subplot(212)
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    # plt.ylim((0.9, 2.2))

    plt.suptitle(args.suptitle)
    plt.tight_layout()
    plt.savefig(figfile)

if __name__ == "__main__":
    args = parse_args()
    plot_history(args.history_csv, args.fig)
