import requests
import os 

def get_all_sittings(legislature_period=10, years=[2025], months=range(1, 13), days=range(1,32), out_folder="data/xml/"): 
    out_folder = f"{out_folder}/{legislature_period}/"
    os.makedirs(out_folder, exist_ok=True)
    
    for year in years: 
        for m in months: 
            for d in days: 
                month = m if m > 9 else f"0{m}"
                day = d if d > 9 else f"0{d}"
                
                filename = f"CRE-{legislature_period}-{year}-{month}-{day}_EN.xml"
                url = f"https://www.europarl.europa.eu/doceo/document/{filename}"

                response = requests.get(url)
                if(response.ok): 
                    print(filename, " - OK")
                    with open(out_folder+filename, "w") as f: 
                        f.write(response.text)
                else: 
                    print(filename, " - Failed")
if __name__ == "__main__":                 
    get_all_sittings()