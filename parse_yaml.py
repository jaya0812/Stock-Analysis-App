import os
import yaml
import pandas as pd

# Set the root folder path
root_folder = r'C:\Users\Test\Downloads\Guvi project 2\Data'

# List to hold individual DataFrames
dfs = []

# Walk through all directories and files
for dirpath, _, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                df = pd.DataFrame(data)
                dfs.append(df)
            
# Concatenate all DataFrames into one
final_df = pd.concat(dfs, ignore_index=True)

final_df.to_csv(r"C:\Users\Test\Downloads\Guvi project 2\main_data.csv",index=False)