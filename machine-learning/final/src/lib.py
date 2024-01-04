import datetime
import pandas as pd
import lib
import holidays

epoch = pd.to_datetime('1970-01-01')

def months_since_epoch(ser):
    return ((ser.dt.year - 1970) * 12 + ser.dt.month ) 


ie_holidays = holidays.Ireland()
def is_ie_holiday(d):
    return d in ie_holidays

def working_day(d):
    if is_ie_holiday(d):
        return 0
    if d.weekday() < 5:
        return 1
    return 0

def working_day_text(d):
    if is_ie_holiday(d):
        return "Non-working Day"
    if d.weekday() < 5:
        return "Working Day"
    return "Non-working Day"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width',None)
from typing import List

PANDEMIC_START = datetime.datetime(2020,3,12,0,0)
PANDEMIC_END = datetime.datetime(2022, 2, 28, 0, 0)

def tee(*args, **kwargs):
    file = kwargs.pop("file",None)
    print(*args, file=None,**kwargs)
    if file is not None:
        print(*args, file=file,**kwargs)

def to_datetime(series):
    return pd.to_datetime(series, format='%Y-%m-%d %H:%M:%S')

def read_csv(fname, *args, **kwargs):
    df = pd.read_csv(fname, *args, **kwargs)
    df.columns = df.columns.str.replace('_',' ')
    df["TIME"] = lib.to_datetime(df["TIME"])
    df["TIME ROUND 5m"] = df["TIME"].dt.round("5min")
    df["LAST UPDATED"] = lib.to_datetime(df["LAST UPDATED"])
    df["STATUS"] = df["STATUS"].str.title()
    # df.sort_values(by=["STATION ID", "TIME"])
    return df

def even_30m_only(df):
    return df[(df["TIME ROUND 5m"].dt.minute % 30) == 0]

# assuming TIME has already been converted to datetime object
# create a column indicating whether the row's delta should be counted towards usage
def create_has_delta_column(df):
    df.sort_values(by=["STATION ID", "TIME"])
    TIME = df["TIME"]
    LAST_UPDATED = df["LAST UPDATED"]
    deltas: List[bool] = []
    five_min_timedelta = pd.Timedelta(minutes=5)
    previous_time = TIME[0] - five_min_timedelta
    previous_station_id = df["STATION ID"][0]
    for i in range(len(TIME)):
        if previous_station_id == df["STATION ID"][i]:
            has_delta = LAST_UPDATED[i] > previous_time
            deltas.append(has_delta)
        else:
            deltas.append(False)

        previous_time = TIME[i]
        previous_station_id = df["STATION ID"][i]

    return pd.Series(deltas,dtype=bool)