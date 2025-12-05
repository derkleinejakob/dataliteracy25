def add_party_orientation_blocks(df): 
    """
    Create broader party blocks
    
    Creates new column "block" with values in (left, greens, social_democratic, christian_conservative, liberal, right_populist)
    No information loss here
    """

    # TODO: add data source for reasoning

    df['block'] = None 

    # left
    df.loc[df['party'].isin(['GUE/NGL','The Left']), 'block'] = 'left'
    # green
    df.loc[df['party'].isin(['Greens/EFA']), 'block'] = 'greens'
    # social democratic
    df.loc[df['party'].isin(['PSE', 'S&D']), 'block'] = 'social_democratic'
    # christian conservative
    df.loc[df['party'].isin(['PPE-DE', 'PPE']), 'block'] = 'christian_conservative'
    # liberal
    df.loc[df['party'].isin(['ELDR','ALDE', 'Renew']), 'block'] = 'liberal'
    # right populist
    df.loc[df['party'].isin(['EFDD', 'EFD','ITS', 'ENF', 'ID', 'IND/DEM', 'ECR', 'UEN', 'EDD']), 'block'] = 'right_populist'

    # df = df.reset_index(drop=True)
    
    return df