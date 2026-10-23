from pathlib import Path
import pandas as pd
from urllib.request import urlretrieve

# The Moodle page's link has a stray trailing quote; keep the URL itself clean.
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv'
DATA = Path(__file__).resolve().parent / 'data' / 'airline_data.csv'
LOCAL_DOWNLOAD = Path.home() / 'Downloads' / 'airline_data.csv'


def load_airline_data():
    if DATA.exists():
        source = DATA
    elif LOCAL_DOWNLOAD.exists():
        source = LOCAL_DOWNLOAD
    else:
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urlretrieve(URL, DATA)
        source = DATA
    return pd.read_csv(source, encoding='ISO-8859-1', dtype={
        'Div1Airport': str, 'Div1TailNum': str,
        'Div2Airport': str, 'Div2TailNum': str,
    })
