import pandas as pd

def load_intensities(filepath="data/intensities.csv"):  
    return pd.read_csv(filepath)
