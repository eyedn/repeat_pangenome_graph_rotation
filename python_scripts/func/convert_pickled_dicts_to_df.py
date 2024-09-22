###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           convert_pickled_dicts_to_df.py
###############################################################################


import os
import sys
import typing
import pickle
import pandas as pd


def convert_pickled_dicts_to_df(dir: os.PathLike) -> pd.DataFrame:

    counter = 0
    combined_df = None
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        # only consider pickle files
        if file.endswith(".pickle") and os.path.isfile(file_path):            
            # extract genome name as the unique row identifier
            g = file.split(".")[0]
            with open(file_path, 'rb') as f:
                try:
                    data: typing.Dict[str, int] = pickle.load(f)
                    temp_df = pd.DataFrame([data], index=[g])
                    if combined_df is None:
                        combined_df = temp_df
                    else:
                        combined_df = pd.concat([combined_df, temp_df], axis=0)
                    counter += 1
                    print(f"{g} added (no. {counter})")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                sys.stdout.flush()
    combined_df.fillna(0, inplace=True)
    return combined_df
