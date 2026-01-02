#%% 
import pandas as pd 
from scripts.preprocessing import add_party_orientation_year_agenda, keep_relevant_legislation_years, remove_commentary, remove_duplicate_speeches, remove_non_party_speeches, remove_repeating_greetings, remove_repeating_endings, rename_party_duplicates, assign_topics
from tqdm import tqdm

# TODO: run through all scripts in preprocessing folder and manipulate df, then output cleaned df
# TODO: is there a smarter way to do this that is less tedious? 
# TODO: remove empty text / text of certain length ? 


LDA_FINISHED = True
MIGRATION_TOPIC_ID = 19 
MIGRATION_TOPIC_THRESHOLD = 0.25 
N_TOPICS = 30 

#%%
if __name__ == "__main__": 
    def save_df(dataframe, path): 
        if path.endswith(".csv"): 
            dataframe.to_csv(path)
        elif path.endswith(".parquet"): 
            dataframe.to_parquet(path)
        else: 
            raise ValueError(f"Unknown output file ending {path}")
    
    def step(dataframe, process): 
        n_before = len(dataframe) 
        dataframe = process(dataframe)
        n_now = len(dataframe) 
        delta_n = n_before - n_now
        if not (delta_n == 0): 
            print(f"Removed {delta_n} rows ({'%.2f' % (delta_n / n_before)})")
        return dataframe
        
    IN_PATH = "data/parllaw/speech_translated.csv"
    OUT_PATH = "data/parllaw/final.parquet"
    OUT_PATH_MIGRATION = "data/parllaw/migration.parquet"

    print("Reading dataset")
    df = pd.read_csv(IN_PATH, index_col=False)
    # order of application matters! e.g. "rename party duplicates" should be run before "add party orientation blocks"
    preprocessing_steps = [remove_non_party_speeches, keep_relevant_legislation_years, remove_duplicate_speeches, add_party_orientation_year_agenda, rename_party_duplicates, remove_commentary, remove_repeating_greetings, remove_repeating_endings, assign_topics]

    n_columns_before = len(df.columns)
    n_before = len(df)
    print(f"Starting with {n_before} rows and {n_columns_before} columns")
    
    for process in tqdm(preprocessing_steps, "Preprocessing data"): 
        df = step(df, process)

    print(f"Done. Now have {len(df)} rows and {len(df.columns)} columns")
    
    if LDA_FINISHED: 
        df["migration_prob"] = df[f"topic_{MIGRATION_TOPIC_ID}"]
        df_migration = df[df["migration_prob"] >= MIGRATION_TOPIC_THRESHOLD]
        df_migration = df_migration.drop(columns=[f"topic_{i}" for i in range(N_TOPICS)])
        save_df(df_migration, OUT_PATH_MIGRATION)
    else: 
        print("Cannot create dataframe with only migration speeches yet. Run LDA first.")

    save_df(df, OUT_PATH)
# %%
