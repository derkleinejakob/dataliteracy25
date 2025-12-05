
def remove_non_party_speeches(df): 
    # df["year"] = df.apply(lambda s: int(s["date"][:4]), axis=1)
    # df["uq_agenda"] = df["agenda"]+df["date"]
    
        # only use speeches where speaker is associated with a party
    return df[~(df["party"] == "-")]

    # TODO: remove NI and TDI as well? 