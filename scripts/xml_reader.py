# NOTE: this was chatgpt generated and contains a small bug that the first paragraph is sometimes accidentally skipped => should be debugged!

import xml.etree.ElementTree as ET

def scan_first_para_children(para): 
    # TODO: check if assumptions are correct for all texts!
    i = 0 
    for child in para: 
        # the first tag is usually italic and contains group membership info
        if child.tag == "EMPHAS" and child.attrib.get("NAME") == "I": 
            print("skipping tag", child.text)
            i += 1 
            continue
        # the first tag is often followed by a bold tag only containing "."
        if child.tag == "EMPHAS" and child.attrib.get("NAME") == "B" and child.text == ".": 
            print("skipping tag", child.text)
            i += 1 
            continue
        # stop scanning after first child that does not match filter pattern
        break 
    # return the index of children to skip (0, 1, or 2 usually)
    return i

def parse_contributions(xml_path, skip_non_party_members = False):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    contributions = []

    # each contribution is in a <intervention>...</intervention> tag
    for intervention in root.findall(".//INTERVENTION"):
        # the information about the speaker is in a <orateur>...</orateur> tag
        # assumption: attributes are PP, LG, MEPID, CODICT, LIB="{name} | {surname}",  SPEAKER_TYPE
        orateur = intervention.find("ORATEUR")
        if orateur is None:
            continue
        
        # TODO: make sure there are no additional attributes here that might be of use / that the format is consistent
        # Speaker name (first and last name)
        # name = orateur.attrib.get("LIB", "").replace("|", " ").strip()

        # # Political group (if available)
        # group = orateur.attrib.get("PP", "").strip()

        if skip_non_party_members and (orateur.attrib.get("PP") is None or orateur.attrib.get("PP") == "NULL"):  
            print("skipping speaker without party membership")
            continue
        
         # Combine all paragraph texts
        para_texts = []
        for i, para in enumerate(intervention.findall("PARA")):
            text_parts = list(para.itertext())
            if i == 0: 
                # Some paragraphs contain a <EMPHAS> tag with information about the speaker's group membership,
                # e.g., <EMPHAS NAME="I">on behalf of the ECR Group</EMPHAS>
                # followed by <EMPHAS NAME="B">.</EMPHAS>
                # -> make sure to skip the first parts of the paragraph if it contains these elements
                
                skip_first_k = scan_first_para_children(para)
                text_parts = text_parts[skip_first_k:]
            para_texts.append("".join(text_parts))

        speech = "\n".join(para_texts)

        contributions.append({
            # "name": name,
            # "group": group,
            # for now: just keep all speaker attributes => can sort some out later
            **orateur.attrib,
            "speech": speech,
        })

    return contributions

if __name__ == "__main__": 
    path = "data/CRE-9-2021-11-23-ITM-010_EN.xml" 
    
    contributions = parse_contributions(path)
    print(contributions)
