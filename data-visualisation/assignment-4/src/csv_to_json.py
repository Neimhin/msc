import sys
import pandas as pd

def csv_to_json(csv_file_path, json_file_path):
    """
    Load a CSV file with pandas and convert it to a JSON file.

    Parameters:
    csv_file_path (str): Path to the input CSV file.
    json_file_path (str): Path to save the output JSON file.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to JSON and save it
    df.to_json(json_file_path, orient='records')

if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    csv_to_json(in_file,out_file)
