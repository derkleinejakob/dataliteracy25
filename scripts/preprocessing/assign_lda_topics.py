from tqdm import tqdm 
from gensim import corpora
import json 
from gensim.models import LdaMulticore
import numpy as np 
import pandas as pd 

def assign_topics(df): 
    # TODO: this needs some fixing (index should not be reset!)
    # TODO: rerun LDA after data is cleaned and make sure preprocessed texts are now just aligned with the df
    
    N_TOPICS = 50 
    LDA_MODEL_PATH = f"data/lda/{N_TOPICS}_topics/10/model.model"

    def assign_topics(lda_model, corpus):
        topics = []
        for bow in tqdm(corpus, desc="Assigning most probable topic to each speech"):
            docs_topics = lda_model.get_document_topics(bow, minimum_probability=0)
            topics.append(docs_topics)
        return topics

    lda_model = LdaMulticore.load(LDA_MODEL_PATH)
    preprocessed_data = json.load(open("data/lda/preprocessed_texts_all_translated.json"))
    # TODO: pretty sure preprocessed_data and df are not yet aligned! we remove additional stuff from df but load old preprocessing file -> redo preprocessing?
    assert len(preprocessed_data) == len(df), "Length of preprocessed data and dataframe do not match!"

    # TODO: outsource this, should be shared with LDA script
    print("Creating dictionary")
    dictionary = corpora.Dictionary(preprocessed_data)

    # TODO: test values
    dictionary.filter_extremes(
        no_below=10,     # Keep tokens appearing in at least 10 docs
        no_above=0.4,    # Remove tokens appearing in more than 40% of docs
        keep_n=100000    # Keep only the top 100k words by frequency
    )
    corpus = [dictionary.doc2bow(l) for l in tqdm(preprocessed_data, "Preparing corpus")]

    corpus_topics = assign_topics(lda_model, corpus)
    # set up df with topic probabilities

    # corpus topics is a list of lists of (topic_id, probability) tuples for each document in the corpus
    # this list is turned into dataframe of size (num_docs, num_topics) with probabilities
    num_docs = len(corpus_topics)
    
    topic_prob_matrix = np.zeros((num_docs, N_TOPICS))
    for doc_idx, doc_topics in enumerate(corpus_topics):
        for topic_id, prob in doc_topics:
            topic_prob_matrix[doc_idx, topic_id] = prob
            
    topic_prob_df = pd.DataFrame(topic_prob_matrix, columns=[f"topic_{i}" for i in range(N_TOPICS)])

    # append topic probabilities to df_party_members
    # TODO: why reset_index?? 
    
    return pd.concat([df.reset_index(drop=True), topic_prob_df], axis=1)

