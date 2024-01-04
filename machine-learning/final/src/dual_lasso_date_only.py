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
usage = global_available_diff.groupby(global_available_diff.index.date).sum()

# convert global_available_diff to a DataFrame with columns
# "TIME ROUND 5m" (global_available_diff.index) "TOTAL AVAILABLE BIKES" (global_available.values)
# "TOTAL AVAILABLE BIKES DIFF ABS" (global_available_diff.values)
usage_df = pd.DataFrame({
    "DATE": usage.index,
    "TOTAL AVAILABLE BIKES DIFF ABS": usage.values
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
usage_df['DATE'] = pd.to_datetime(usage_df['DATE'])
usage_df["Workday (hols)"] = usage_df['DATE'].map(lib.working_day)
usage_df['Minutes'] = usage_df['DATE'].apply(lambda x: x.timestamp())
# df_global_available_diff['Workday'] = df_global_available_diff['TIME ROUND 5m'].dt.weekday < 5  # Monday=0, Sunday=6
# day_of_year = df_global_available_diff['TIME ROUND 5m'].dt.dayofyear
# df_global_available_diff['Day of Year Squared'] = np.square(df_global_available_diff['Day of Year'])
month_one_hot = pd.get_dummies(usage_df["DATE"].dt.month,prefix="Month")
# interval = usage_df['TIME ROUND 5m'].dt.hour * 2 + usage_df['TIME ROUND 5m'].dt.minute // 30
# intervals_one_hot = pd.get_dummies(interval, prefix='Interval')
usage_df = pd.concat([usage_df, month_one_hot], axis=1)

print(usage_df.head())

from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold, GridSearchCV

features = ["Minutes", "Workday (hols)"] + [col for col in usage_df.columns if col.startswith("Month")]
X = usage_df[features]
y = usage_df["TOTAL AVAILABLE BIKES DIFF ABS"].fillna(0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Define the range of C values to explore for each model
C_values = np.logspace(-4, 4, 30)
alpha_values = 1 / C_values  # Convert C values to alpha values for Lasso

# Initialize KFold for cross-validation
cv = KFold(n_splits=5, shuffle=False)

# Prepare to track best models for each subset
model_workday = None
model_non_workday = None

# Subset 1: Where "Workday (hols)" = True
X_workday = X_train[X_train['Workday (hols)'] == 1]
y_workday = y_train[X_train['Workday (hols)'] == 1]

# GridSearch to find the best C for Workday subset
lasso_grid_workday = GridSearchCV(Lasso(), param_grid={'alpha': alpha_values}, cv=cv, scoring='neg_mean_squared_error')
lasso_grid_workday.fit(X_workday, y_workday)

# Best model for Workday
model_workday = Lasso(alpha=lasso_grid_workday.best_params_['alpha'])
model_workday.fit(X_workday, y_workday)

# Subset 2: Where "Workday (hols)" = False
X_non_workday = X_train[X_train['Workday (hols)'] == 0]
y_non_workday = y_train[X_train['Workday (hols)'] == 0]

# GridSearch to find the best C for Non-Workday subset
lasso_grid_non_workday = GridSearchCV(Lasso(), param_grid={'alpha': alpha_values}, cv=cv, scoring='neg_mean_squared_error')
lasso_grid_non_workday.fit(X_non_workday, y_non_workday)

# Best model for Non-Workday
model_non_workday = Lasso(alpha=lasso_grid_non_workday.best_params_['alpha'])
model_non_workday.fit(X_non_workday, y_non_workday)

# Now you have two models: best_lasso_workday and best_lasso_non_workday
# You can use these models to make predictions and evaluate their performance
def evaluate_dual_model(X, y, model_workday, model_non_workday):
    workday_filter = X['Workday (hols)'] == 1
    non_workday_filter = X['Workday (hols)'] == 0
    y_pred = np.zeros_like(y)
    y_pred[workday_filter] = model_workday.predict(X[workday_filter])
    y_pred[non_workday_filter] = model_non_workday.predict(X[non_workday_filter])
    mse = mean_squared_error(y, y_pred)
    return mse

def evaluate_baseline(X,y):
    workday_mean = y_train[X_train['Workday (hols)'] == 1].mean()
    non_workday_mean = y_train[~(X_train['Workday (hols)'] == 1)].mean()
    print("workday mean", workday_mean)
    print("non workday mean", non_workday_mean)
    predictions = X['Workday (hols)'].apply(lambda x: workday_mean if x else non_workday_mean)
    mse = mean_squared_error(y, predictions)
    return mse
   
mse_test_dual_model = evaluate_dual_model(X_test, y_test, model_workday, model_non_workday)
mse_baseline = evaluate_baseline(X_test,y_test)

print("dual model mse:", mse_test_dual_model)
print("baseline model mse:", mse_baseline)