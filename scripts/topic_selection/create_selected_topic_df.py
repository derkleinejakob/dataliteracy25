from gensim.models import LdaMulticore
import numpy as np 
import pandas as pd 

def create_selected_topic_df(topic_id, topic_name,prob_threshold, top_n = 10):
    '''
    Create and save dataframe for speeches related to a specific topic identified by a keyword.
    Parameters:
    - df: pd.DataFrame, dataframe with speeches and topic probabilities
    - model: LdaModel, trained LDA model
    - keyword: str, keyword to identify the topic
    - prob_threshold: float, probability threshold to select speeches
    - top_n: int, number of top words to consider for topic matching
    - n_topics: int, total number of topics in the model
    Returns:
    - df_selected_topic: pd.DataFrame, dataframe with speeches related to the selected topic
    '''
    DF_IN_PATH = "data/parllaw/final.csv"
    DF_OUT_PATH = f"data/lda/selected_topic_data/df_{topic_name}.csv"
    N_TOPICS = 50 
    LDA_MODEL_PATH = f"data/lda/{N_TOPICS}_topics/10/model.model"

    model = LdaMulticore.load(LDA_MODEL_PATH)
    df = pd.read_csv(DF_IN_PATH)
    
    print(f"Creating dataframe for topic {topic_id} named '{topic_name}'.")
    df_selected_topic = df[df[f'topic_{topic_id}'] >= prob_threshold].copy()
    df_selected_topic.to_csv(DF_OUT_PATH, index=False)
    print(f"Saved dataframe with {df_selected_topic.shape[0]} speeches to {DF_OUT_PATH}")
    return df_selected_topic