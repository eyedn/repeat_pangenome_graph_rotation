###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           gather_rare_counts.py
###############################################################################


from sys import argv
import os
import sys
import pickle
import pandas as pd


def convert_pickled_dicts_to_df(dir: os.PathLike) -> pd.DataFrame:

    all_data = []
    columns = set()  # Track all possible column names
    counter = 0

    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if file.endswith(".pickle") and os.path.isfile(file_path):
            genome = file.split(".")[0]
            with open(file_path, 'rb') as f:
                try:
                    data = pickle.load(f)
                    # Add all keys to the column set
                    columns.update(data.keys())
                    all_data.append((genome, data))
                    counter += 1
                    print(f"{genome} added (no. {counter})")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                sys.stdout.flush()

    # create a DataFrame with all collected data
    combined_df = pd.DataFrame(index=[x[0] for x in all_data], columns=sorted(columns))
    # fill the DataFrame with 0s or 1s
    for genome, data in all_data:
        combined_df.loc[genome] = pd.Series(data)
    return combined_df.astype(int)

if __name__ == "__main__":
    dir = argv[1]
    out = argv[2]

    combined_dict = convert_pickled_dicts_to_df(dir)
    combined_dict.to_csv(out)
