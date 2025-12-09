import pandas as pd
import textwrap
from IPython.display import clear_output

def sample_and_rate_topic(df_topics, topic_id,  n_speeches = 100, seed = 42, lower_prob=0.25, upper_prob=0.45):
    """
    Randomly sample speeches whose topic probability is within [lower_prob, upper_prob],
    show translatedText, and collect manual ratings (1 = belongs, 0 = not).
    Returns a DataFrame with columns ['probability', 'rating'] of length n (or fewer if not enough speeches).
    """

    prob_col = f"topic_{topic_id}"
    candidates = df_topics[(df_topics[prob_col] >= lower_prob) & (df_topics[prob_col] <= upper_prob)]
    
    sampled = candidates.sample(n=min(n, len(candidates)), random_state=seed).reset_index(drop=True)
    ratings = []
    
    for i, row in sampled.iterrows():
        clear_output(wait=True)
        print(f"Progress: {i+1}/{len(sampled)} speeches rated")
        print(f"\nSpeech {i+1}/{len(sampled)} | Year: {row['year']} | Party block: {row['party_block']}")
        print(f"Topic probability: {row[prob_col]:.4f}")
        print(textwrap.fill(row["translatedText"], width=90))
        
        while True:
            user_input = input("\nRate this speech (1 = belongs to topic, 0 = not, q = quit): ").strip()
            if user_input in {"0", "1"}:
                ratings.append(int(user_input))
                break
            elif user_input.lower() == "q":
                print(f"\nRating interrupted. Returning {len(ratings)} ratings collected so far.")
                result = pd.DataFrame({
                    "probability": sampled[prob_col].iloc[:len(ratings)].values,
                    "rating": ratings
                })
                return result
            else:
                print("Please enter 0, 1, or q to quit.")
    
    clear_output(wait=True)
    print(f"Rating complete! Rated {len(ratings)}/{len(sampled)} speeches.")
    
    result = pd.DataFrame({
        "probability": sampled[prob_col].values,
        "rating": ratings
    })
    return result