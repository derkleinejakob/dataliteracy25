from tueplots.constants.color import rgb

PATH_RAW_DATA = "data/intermed/speech_output.csv"
PATH_TRANSLATED_DATA = "data/intermed/speech_translated.parquet"
PATH_DF_TRANSLATION_TEST = "data/translation/df_translation_test.parquet"

PATH_ALL_SPEECHES = "data/final/full.parquet" # formerly known as final.parquet
PATH_MIGRATION_SPEECHES = "data/final/migration.parquet" 
PATH_MIGRATION_SPEECHES_EMBEDDED = "data/final/migration_with_embeddings.parquet" # formerly known as SPEECH_EMBEDDINGS.parquet
PATH_VOCAB_EMBEDDED = "data/final/vocab_embeddings.parquet" # formerly known as VOCAB_EMBEDDGINGS.parquet
PATH_MODEL = "data/lda/final_model/model.model"

COLOR_MAP_PARTY = {
    "PSE/S&D": "#E41A1C",
    
    "Greens/EFA": "#32CD32",

    "ELDR/ALDE/Renew": "#FFD700",     

    "PPE": "#1F77B4",      
    "PPE-DE": "#1E90FF",   
    "UEN": "#F4D03F",      

    "ECR": "#0057A4",      
    "EDD/INDDEM/EFD": "#6A5ACD",  
    "EFD": "#7B68EE",      
    "EFDD": "#9370DB",     

    "ITS": "#00008B",     
    "ENF/ID": "#000080",      

    "NGL/The Left": "#8B0000",
}

# use Uni Tübingen corporate design? 
COLOR_MAP_BLOCK = { 
    "left": rgb.tue_violet,
    "green": rgb.tue_green,
    "social_democratic": rgb.tue_red,
    "christian_conservative": "black",
    "liberal": rgb.tue_orange,
    "(extreme)_right": rgb.tue_blue,
}

COLOR_MAPS = {
    "party": COLOR_MAP_PARTY,
    "block": COLOR_MAP_BLOCK,
}

ELECTION_YEARS = [1999, 2004, 2009, 2014, 2019, 2024]

EMBEDDING_MODEL = "google/embeddinggemma-300m"

N_TOPICS = 30
