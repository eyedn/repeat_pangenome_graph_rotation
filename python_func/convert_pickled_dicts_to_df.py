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


from collections import defaultdict
import os
import pickle
import pandas as pd


def convert_pickled_dicts_to_dfs(dir: os.PathLike) -> pd.DataFrame:

    combined_dict = defaultdict(int) 
    # get all pickled dict in dir
    for files in os.listdir(dir):
        for file in files:
            if file.endswith('.pickle'):
                file_path = os.path.join(dir, file)
                # load pickled dict
                with open(file_path, 'rb') as f:
                    try:
                        data = pickle.load(f)
                        # sum values of common keys
                        if isinstance(data, dict):
                            for key, value in data.items():
                                combined_dict[key] += value
                        else:
                            print(f"Error: {file_path} not a dict")
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
    combioned_df = pd.DataFrame(dict(combined_dict))
    return combioned_df
