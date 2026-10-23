from pathlib import Path
import pandas as pd
from urllib.request import urlretrieve

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv'
DATA = Path(__file__).resolve().parent / 'data' / 'Historical_Wildfires.csv'
LOCAL_DOWNLOAD = Path.home() / 'Downloads' / 'Historical_Wildfires.csv'


def load_wildfire_data():
    if DATA.exists():
        source = DATA
    elif LOCAL_DOWNLOAD.exists():
        source = LOCAL_DOWNLOAD
    else:
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urlretrieve(URL, DATA)
        source = DATA
    return pd.read_csv(source)
