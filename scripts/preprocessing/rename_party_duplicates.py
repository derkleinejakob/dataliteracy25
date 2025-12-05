def rename_party_duplicates(df): 
    """
    Merge parties that changed over time
    
    Changes party column
    Information loss: because old party names are not kept
    """
    
    # TODO add data source for reasoning
    
    df['party_adj'] = None 

    pse_snd = ['PSE', 'S&D']
    ppe = ['PPE-DE', 'PPE']
    efd = ['EFDD', 'EFD']
    enf_id = ['ITS', 'ENF', 'ID']
    eldr_alde_renew = ['ELDR','ALDE', 'Renew']
    ngl_theleft = ['GUE/NGL','The Left']
    eed = ['IND/DEM','EDD']
    

    # make sure we handle all parties here: 
    assert df['party'].isin([
        *pse_snd, *ppe, *efd, *enf_id, *eldr_alde_renew, *ngl_theleft, *eed, 
    ]).all()

    df.loc[df['party'].isin(pse_snd), 'party_adj'] = 'PSE/S&D' # PSE becomes S&D
    df.loc[df['party'].isin(ppe), 'party_adj'] = 'PPE' # PPE-DE' becomes 'PPE'
    df.loc[df['party'].isin(efd), 'party_adj'] = 'EFD' # 'EFDD' becomes 'EFD'
    df.loc[df['party'].isin(enf_id), 'party_adj'] = 'ENF/ID' # ENF becomes ID in 2019
    df.loc[df['party'].isin(eldr_alde_renew), 'party_adj'] = 'ELDR/ALDE/Renew' # ELDR becomes ALDE becomes Renew
    df.loc[df['party'].isin(ngl_theleft), 'party_adj'] = 'NGL/The Left' # GUE/NGL becomes The Left
    df.loc[df['party'].isin(eed), 'party_adj'] = 'INDDEM/EDD' # independents become EDD


    df.drop('party', axis=1, inplace=True)
    df = df.rename(columns={'party_adj': 'party'})

    return df 