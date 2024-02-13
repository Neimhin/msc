import datetime
import pandas as pd
import lib
import holidays
import numpy as np
from sklearn.metrics import mean_squared_error

epoch = pd.to_datetime('1970-01-01')

def months_since_epoch(ser):
    return ((ser.dt.year - 1970) * 12 + ser.dt.month ) 


def dual_model_predict(X,y,model_workday,model_non_workday):
    workday_filter = X['Workday (hols)'] == 1
    non_workday_filter = X['Workday (hols)'] == 0
    y_pred = np.zeros_like(y)
    y_pred[workday_filter] = model_workday.predict(X[workday_filter])
    y_pred[non_workday_filter] = model_non_workday.predict(X[non_workday_filter])
    return y_pred

def evaluate_dual_model(X, y, model_workday, model_non_workday, grouper=None):
    print(X.index)
    print(y.index)
    y_pred = dual_model_predict(X,y,model_workday,model_non_workday)
    if grouper:
        y_pred = pd.Series(y_pred,index=y.index)
        y = y.groupby(grouper).sum()
        y_pred = y_pred.groupby(grouper).sum()
    mse = mean_squared_error(y, y_pred)
    return mse

def evaluate_baseline(X,y,X_train,y_train,grouper=None):
    workday_mean = y_train[X_train['Workday (hols)'] == 1].mean()
    non_workday_mean = y_train[~(X_train['Workday (hols)'] == 1)].mean()
    predictions = X['Workday (hols)'].apply(lambda x: workday_mean if x else non_workday_mean)
    if grouper:
        predictions = predictions.groupby(grouper).sum()
        y = y.groupby(grouper).sum()
    mse = mean_squared_error(y, predictions)
    return mse

# def evaluate_baseline_group_first(X,y,X_train,y_train,grouper=None):
#     print(y_train)
#     if grouper:
#         y = y.groupby(grouper).sum()
#         X = X.groupby(grouper).sum()
#         X_train = X_train.groupby(grouper).sum()
#         y_train = y_train.groupby(grouper).sum()
#     print(X_train)
#     workday_mean = y_train[X_train['Workday (hols)'] == 1].mean()
#     non_workday_mean = y_train[~(X_train['Workday (hols)'] == 1)].mean()
#     print(workday_mean)
#     print(non_workday_mean)
#     print(y.isna().sum())
#     print(y_train.isna().sum())
#     predictions = X['Workday (hols)'].apply(lambda x: workday_mean if x else non_workday_mean)
#     mse = mean_squared_error(y, predictions)
#     return mse

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