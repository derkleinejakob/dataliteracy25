import pandas as pd 

def add_party_orientation_blocks(filename="data/parllaw/speech_translated.csv"): 
    # import parllaw speech dataset
    df = pd.read_csv(filename)
    df["year"] = df.apply(lambda s: int(s["date"][:4]), axis=1)
    df["uq_agenda"] = df["agenda"]+df["date"]
    
    print(len(df), "speeches in total")
    # only use speeches where speaker is associated with a party
    df_party_members = df[~(df["party"] == "-")]

    # only keep speeches with at least 50 characters: important for coherence with preprocessed data
    df_party_members = df_party_members[df_party_members["translatedText"].map(str).map(len) > 50]
    print(len(df_party_members), "speeches of party members (longer than 50 characters)")
    
    # merge parties that changed names over time
    df_party_members['party_adj'] = df_party_members['party']  # start with a copy

    df_party_members.loc[df_party_members['party'].isin(['PSE', 'S&D']), 'party_adj'] = 'PSE/S&D' # PSE becomes S&D
    df_party_members.loc[df_party_members['party'].isin(['PPE-DE', 'PPE']), 'party_adj'] = 'PPE' # PPE-DE' becomes 'PPE'
    df_party_members.loc[df_party_members['party'].isin(['EFDD', 'EFD']), 'party_adj'] = 'EFD' # 'EFDD' becomes 'EFD'
    df_party_members.loc[df_party_members['party'].isin(['ITS', 'ENF', 'ID']), 'party_adj'] = 'ENF/ID' # ENF becomes ID in 2019
    df_party_members.loc[df_party_members['party'].isin(['ELDR','ALDE', 'Renew']), 'party_adj'] = 'ELDR/ALDE/Renew' # ELDR becomes ALDE becomes Renew
    df_party_members.loc[df_party_members['party'].isin(['GUE/NGL','The Left']), 'party_adj'] = 'NGL/The Left' # GUE/NGL becomes The Left
    df_party_members.loc[df_party_members['party'].isin(['IND/DEM','EDD']), 'party_adj'] = 'INDDEM/EDD' # independents become EDD

    # create broader party blocks
    df_party_members['party_block'] = df_party_members['party']  # start with a copy

    # left
    df_party_members.loc[df_party_members['party'].isin(['GUE/NGL','The Left']), 'party_block'] = 'left'
    # green
    df_party_members.loc[df_party_members['party'].isin(['Greens/EFA']), 'party_block'] = 'greens'
    # social democratic
    df_party_members.loc[df_party_members['party'].isin(['PSE', 'S&D']), 'party_block'] = 'social_democratic'
    # christian conservative
    df_party_members.loc[df_party_members['party'].isin(['PPE-DE', 'PPE']), 'party_block'] = 'christian_conservative'
    # liberal
    df_party_members.loc[df_party_members['party'].isin(['ELDR','ALDE', 'Renew']), 'party_block'] = 'liberal'
    # right populist
    df_party_members.loc[df_party_members['party'].isin(['EFDD', 'EFD','ITS', 'ENF', 'ID', 'IND/DEM', 'ECR', 'UEN', 'EDD']), 'party_block'] = 'right_populist'

    df_party_members = df_party_members.reset_index(drop=True)
    
    return df, df_party_members