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

def working_day(d):
    if is_ie_holiday(d):
        return 0
    if d.weekday() < 5:
        return 1
    return 0


# Set up KFold with no shuffling
cv = KFold(n_splits=5, shuffle=False)

# Step 1: Prepare the data with additional features
df_global_available_diff['TIME ROUND 5m'] = pd.to_datetime(df_global_available_diff['TIME ROUND 5m'])
df_global_available_diff["Workday (hols)"] = df_global_available_diff['TIME ROUND 5m'].map(lib.working_day)
df_global_available_diff['Minutes'] = df_global_available_diff['TIME ROUND 5m'].apply(lambda x: x.timestamp())
df_global_available_diff['Workday'] = df_global_available_diff['TIME ROUND 5m'].dt.weekday < 5  # Monday=0, Sunday=6
df_global_available_diff['Day of Year'] = df_global_available_diff['TIME ROUND 5m'].dt.dayofyear
df_global_available_diff['Day of Year Squared'] = np.square(df_global_available_diff['Day of Year'])

# Step 2: Subset the data by date
subset_df = df_global_available_diff[df_global_available_diff['TIME ROUND 5m'] < lib.PANDEMIC_START]

# Visualize the results
plt.figure()

def cross_val_with_features(features):
    X = subset_df[features]
    y = subset_df['TOTAL AVAILABLE BIKES DIFF ABS'].fillna(0)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lasso_cv = LassoCV(alphas=np.logspace(-4, 4, 30), cv=cv, random_state=42)
    lasso_cv.fit(X, y)
    plt.errorbar(1/lasso_cv.alphas_, lasso_cv.mse_path_.mean(axis=-1), yerr=lasso_cv.mse_path_.std(axis=-1), label=f"{features}")

cross_val_with_features(["Minutes"])
cross_val_with_features(["Minutes", "Workday"])
cross_val_with_features(["Minutes", "Workday (hols)"])
cross_val_with_features(["Minutes", "Day of Year Squared"])

plt.legend()

plt.xscale('log')
plt.xlabel('Hyperparameter C')
plt.ylabel('Mean square error')
plt.title('Cross-Validation Results')
plt.savefig(directory + "/lasso_cross_val.pdf")
