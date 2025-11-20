from gensim import corpora
from gensim.models import LdaModel, LdaMulticore
from gensim.utils import simple_preprocess
import spacy
import logging
from typing import List
from tqdm import tqdm
from multiprocessing import Pool
from joblib import Parallel, delayed
import json 

def preprocess_text(nlp, document, custom_stopwords=[]):    
    # tokenize 
    tokens = simple_preprocess(document)
    document = nlp(" ".join(tokens))
    # lemmatize and remove stopwords 
    lemmas = [token.lemma_ for token in document if (not token.is_stop) and (not token.lemma_ in custom_stopwords)]
    return lemmas

def process_texts(documents: List[str], custom_stopwords, test_first_k = None, out_path_processed="lda/preprocessed_texts.json", out_path="lda.model", num_topics=30, n_passes=10, workers=4): 
    logging.basicConfig(format ='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level = logging.WARN)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    if test_first_k: 
        documents = documents[:test_first_k]
    
    processed_data = [preprocess_text(nlp, doc, custom_stopwords) for doc in tqdm(documents, "preprocessing")]
    json.dump(processed_data, open(out_path_processed, "w+"))
    
    dictionary = corpora.Dictionary(processed_data)
    corpus = [dictionary.doc2bow(l) for l in processed_data]
    # Training and Saving model
    print("Fitting model")
    lda_model = LdaMulticore(corpus = corpus, id2word=dictionary, num_topics = num_topics, passes = n_passes, workers=workers)
    lda_model.save(out_path)
    for idx, topic in lda_model.show_topics(formatted=False, num_topics=num_topics):
        label = ", ".join([word for word, prob in topic[:3]])
        print(f"Topic {idx + 1}: {label}")
        
    return lda_model, processed_data

#%% 
if __name__ == "__main__":
    import pandas as pd 
    print("reading dataset")
    filename = "data/parlaw/speech_output.csv"
    df = pd.read_csv(filename)
    df_party_members = df[~(df["party"] == "-")]

#%%
if __name__ == "__main__":
    documents = df_party_members["translatedText"].dropna().to_list()

    model = process_texts(documents, test_first_k=100, num_topics=2, n_passes=1)