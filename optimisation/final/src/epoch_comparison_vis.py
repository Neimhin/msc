import pandas as pd
import matplotlib.pyplot as plt

plt.figure()

def batch_size_to_color(batch_size):
    powers_of_two = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    
    # Define a color map for categorical colors
    colors = plt.cm.tab10.colors  # This gives a list of 10 colors
    
    # Create a dictionary to map batch sizes to colors
    color_dict = {}
    
    for idx, size in enumerate(powers_of_two):
        if size <= batch_size:
            c = colors[idx % len(colors)]
            c = (c[0], c[1], c[2], 0.7)
            color_dict[size] = c
    
    # If batch size is not a power of 2, return a default color
    if batch_size not in color_dict:
        color_dict[batch_size] = 'grey'
    
    return color_dict[batch_size]

for batch_size in [1, 8, 16, 32, 64, 128, 1024, 2048, 4096]:
    color = batch_size_to_color(batch_size)
    for fold in [0, 1, 2, 3, 4]:
        exp = f"exp/{batch_size}/{fold}"
        history = pd.read_csv(exp +  "/history.csv")
        epoch = list(range(len(history)))
        val_label = str(batch_size) + " val" if fold == 0 else None
        train_label = str(batch_size) + " train" if fold == 0 else None
        plt.plot(epoch, history["val_loss"], color=color, label=val_label, lw=0.8)
        plt.plot(epoch, history["loss"], color=color, label=train_label, lw=0.8, linestyle='--')
plt.legend(loc="upper right")
plt.xlabel("epoch")
plt.xlim(0, 80)
plt.ylabel("$\mathcal{L}(\\theta)$")
plt.savefig("fig/epoch_comparison_vis.pdf")
plt.show()
