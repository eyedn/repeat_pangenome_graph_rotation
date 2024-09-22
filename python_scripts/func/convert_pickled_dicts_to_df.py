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
import typing
import pickle
import pandas as pd


def convert_pickled_dicts_to_df(dir: os.PathLike) -> pd.DataFrame:

    combined_df = None
    for i, file in enumerate(os.listdir(dir)):
        file_path = os.path.join(dir, file)
        # only consider pickle files
        if file.endswith('.pickle') and os.path.isfile(file_path):            
            # extract genome name as the unique row identifier
            g = file.split("/")[-1].split(".")[0]
            print(f"adding {g}")
            with open(file_path, 'rb') as f:
                try:
                    data: typing.Dict[str, int] = pickle.load(f)
                    temp_df = pd.DataFrame([data], index=[g])
                    if combined_df is None:
                        combined_df = temp_df
                    else:
                        combined_df = pd.concat([combined_df, temp_df], axis=0)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        if 1 == 10:
            break
    combined_df.fillna(0, inplace=True)
    return combined_df
