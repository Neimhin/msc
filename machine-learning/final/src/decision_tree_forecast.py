from random import shuffle
from click import DateTime
import pandas as pd
import argparse
import lib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import holidays
from sklearn.metrics import mean_squared_error
import holidays

ie_holidays = holidays.Ireland()
def is_ie_holiday(d):
    return d in ie_holidays

def working_day(d):
    if is_ie_holiday(d):
        return 0
    if d.weekday() < 6:
        return 1
    return 0

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--input",type=str)
arg = argument_parser.parse_args()
print(arg.input)
directory = arg.input + ".d"
os.makedirs(directory,exist_ok=True)

# part 1: load the data
df = lib.read_csv(arg.input)
df = lib.even_30m_only(df)

global_available = df.groupby("TIME ROUND 5m")["AVAILABLE BIKES"].sum()
global_available_diff = global_available.diff().abs()

# convert global_available_diff to a DataFrame with columns
# "TIME ROUND 5m" (global_available_diff.index) "TOTAL AVAILABLE BIKES" (global_available.values)
# "TOTAL AVAILABLE BIKES DIFF ABS" (global_available_diff.values)
df_global_available_diff = pd.DataFrame({
    "TIME ROUND 5m": global_available_diff.index,
    "TOTAL AVAILABLE BIKES": global_available.values,
    "TOTAL AVAILABLE BIKES DIFF ABS": global_available_diff.values
})
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split, TimeSeriesSplit
import matplotlib.pyplot as plt
from datetime import datetime
import lib
from sklearn.model_selection import KFold

# Step 1: Prepare the data with additional features
df_global_available_diff['TIME ROUND 5m'] = pd.to_datetime(df_global_available_diff['TIME ROUND 5m'])
df_global_available_diff["Workday (hols)"] = df_global_available_diff['TIME ROUND 5m'].map(lib.working_day)
df_global_available_diff['Minutes'] = df_global_available_diff['TIME ROUND 5m'].apply(lambda x: x.timestamp())
df_global_available_diff['Workday'] = df_global_available_diff['TIME ROUND 5m'].dt.weekday < 5  # Monday=0, Sunday=6
df_global_available_diff['Day of Year'] = df_global_available_diff['TIME ROUND 5m'].dt.dayofyear
df_global_available_diff['Day of Year Squared'] = np.square(df_global_available_diff['Day of Year'])

df_global_available_diff['Interval'] = df_global_available_diff['TIME ROUND 5m'].dt.hour * 2 + df_global_available_diff['TIME ROUND 5m'].dt.minute // 30
intervals_one_hot = pd.get_dummies(df_global_available_diff['Interval'], prefix='Interval')
df_global_available_diff = pd.concat([df_global_available_diff, intervals_one_hot], axis=1)

print(df_global_available_diff.head())

from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold, GridSearchCV

features = ["Minutes", "Workday (hols)"] + [col for col in df_global_available_diff.columns if col.startswith("Interval")]
X = df_global_available_diff[features]
y = df_global_available_diff["TOTAL AVAILABLE BIKES DIFF ABS"].fillna(0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.tree import DecisionTreeRegressor

for i in range(4):
    dt_regressor = DecisionTreeRegressor(max_depth=i+1)  # Start with a small tree to prevent overfitting
    dt_regressor.fit(X_train, y_train)
    y_pred_dt = dt_regressor.predict(X_test)
    mse_dt = mean_squared_error(y_test, y_pred_dt)
    print(f"Decision Tree Depth {i} MSE:", mse_dt)
    from sklearn.tree import plot_tree
    import matplotlib.pyplot as plt