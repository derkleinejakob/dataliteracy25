import sys
from pathlib import Path
import os 

# add project root to sys path to be able to import ./src in notebooks that are in ./experiments
project_root = Path.cwd().parent
sys.path.append(str(project_root))

# change working directory to root so we can open data/file.csv from notebooks in ./experiments 
# and dont have to open ../data/file.csv
os.chdir(project_root)