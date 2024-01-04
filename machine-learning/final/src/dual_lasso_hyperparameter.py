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
min_timestamp = df["TIME"].min().timestamp()
df_global_available_diff['TIME ROUND 5m'] = pd.to_datetime(df_global_available_diff['TIME ROUND 5m'])
df_global_available_diff["Workday (hols)"] = df_global_available_diff['TIME ROUND 5m'].map(lib.working_day)
df_global_available_diff['Minutes'] = df_global_available_diff['TIME ROUND 5m'].apply(lambda x: x.timestamp() - min_timestamp)
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

# Extract mean scores and standard deviations from the cross-validation results for workday and non-workday models
workday_mean_scores = -lasso_grid_workday.cv_results_['mean_test_score']
workday_std_scores = lasso_grid_workday.cv_results_['std_test_score']
non_workday_mean_scores = -lasso_grid_non_workday.cv_results_['mean_test_score']
non_workday_std_scores = lasso_grid_non_workday.cv_results_['std_test_score']

# Create subplots
fig, ax = plt.subplots(1, 2, figsize=(8, 4))
# Plot for Workday Model
ax[0].errorbar(alpha_values, workday_mean_scores, yerr=workday_std_scores, fmt='o', color='b', elinewidth=0.8, capsize=2)
ax[0].set_title('Workday Model Tuning')
ax[0].set_xlabel('Alpha')
ax[0].set_ylabel('Mean Squared Error')
ax[0].set_xscale('log')
ax[0].invert_xaxis()

# Plot for Non-Workday Model
ax[1].errorbar(alpha_values, non_workday_mean_scores, yerr=non_workday_std_scores, fmt='o', color='r', elinewidth=0.8, capsize=2)
ax[1].set_title('Non-Workday Model Tuning')
ax[1].set_xlabel('Alpha')
ax[1].set_ylabel('Mean Squared Error')
ax[1].set_xscale('log')
ax[1].invert_xaxis()
plt.tight_layout()
plt.savefig(directory + "/dual_lasso_hyperparameter_tuning.pdf")

workday_alpha = 0.01
non_workday_alpha = 0.01