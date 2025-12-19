#%% 
import pandas as pd 
from scripts.preprocessing import remove_non_party_speeches, rename_party_duplicates, add_party_orientation_year_agenda, remove_commentary, remove_repeating_greetings, remove_repeating_endings
from tqdm import tqdm

# TODO: run through all scripts in preprocessing folder and manipulate df, then output cleaned df
# TODO: is there a smarter way to do this that is less tedious? 
# TODO: remove empty text / text of certain length ? 

if __name__ == "__main__": 
    IN_PATH = "data/parllaw/speech_translated.csv"
    OUT_PATH = "data/parllaw/final.parquet"
    
    print("Reading dataset")
    df = pd.read_csv(IN_PATH, index_col=False)
    # order of application matters! e.g. "rename party duplicates" should be run before "add party orientation blocks"
    preprocessing_steps = [remove_non_party_speeches, rename_party_duplicates, add_party_orientation_year_agenda, remove_commentary, remove_repeating_greetings, remove_repeating_endings]

    n_columns_before = len(df.columns)
    n_before = len(df)
    print(f"Starting with {n_before} rows and {n_columns_before} columns")
    
    for process in tqdm(preprocessing_steps, "Preprocessing data"): 
        df = process(df)
        
    print(f"Done. Now have {len(df)} rows and {len(df.columns)} columns")
    
    df.to_csv(OUT_PATH, index=False)
# %%
