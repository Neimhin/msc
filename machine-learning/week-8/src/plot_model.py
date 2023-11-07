import sys
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model

if len(sys.argv) != 2:
    print("Usage: python script_name.py path_to_model.h5")
    sys.exit(1)

model_path = sys.argv[1]

# Check if the given path exists
if not os.path.exists(model_path):
    print(f"Model file {model_path} does not exist!")
    sys.exit(1)
model = load_model(model_path)

# Plot the model architecture to PDF
output_filename = os.path.splitext(os.path.basename(model_path))[0] + ".pdf"
plot_model(model,
    to_file=output_filename,
    show_shapes=True,
    show_layer_names=True,
    )

print(f"Saved model architecture to {output_filename}")