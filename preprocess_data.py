#%% 
import pandas as pd 
from scripts.preprocessing import add_party_orientation_year_agenda, keep_relevant_legislation_years, remove_commentary, remove_duplicate_speeches, remove_non_party_speeches, remove_repeating_greetings, remove_repeating_endings, rename_party_duplicates
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
    preprocessing_steps = [remove_non_party_speeches, keep_relevant_legislation_years, remove_duplicate_speeches, add_party_orientation_year_agenda, rename_party_duplicates, remove_commentary, remove_repeating_greetings, remove_repeating_endings]

    n_columns_before = len(df.columns)
    n_before = len(df)
    print(f"Starting with {n_before} rows and {n_columns_before} columns")
    
    for process in tqdm(preprocessing_steps, "Preprocessing data"): 
        n_before = len(df) 
        df = process(df)
        n_now = len(df) 
        delta_n = n_before - n_now
        if not (delta_n == 0): 
            print(f"Removed {delta_n} rows ({'%.2f' % (delta_n / n_before)})")
        
    print(f"Done. Now have {len(df)} rows and {len(df.columns)} columns")
    
    if OUT_PATH.endswith(".csv"): 
        df.to_csv(OUT_PATH, index=False)
    elif OUT_PATH.endswith(".parquet"): 
        df.to_parquet(OUT_PATH, index=False)
    else: 
        raise ValueError(f"Unknown output file ending {OUT_PATH}")
