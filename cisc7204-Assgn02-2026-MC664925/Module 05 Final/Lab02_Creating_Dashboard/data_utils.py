from pathlib import Path
import pandas as pd
from urllib.request import urlretrieve

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
DATA = Path(__file__).resolve().parent / 'data' / 'automobile-sales.csv'
LOCAL_DOWNLOAD = Path.home() / 'Downloads' / 'automobile-sales.csv'


def load_automobile_data():
    if DATA.exists():
        source = DATA
    elif LOCAL_DOWNLOAD.exists():
        source = LOCAL_DOWNLOAD
    else:
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urlretrieve(URL, DATA)
        source = DATA
    df = pd.read_csv(source)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        if c.lower() == 'unemployment_rate' and c != 'unemployment_rate':
            df.rename(columns={c: 'unemployment_rate'}, inplace=True)
    return df
