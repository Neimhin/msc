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

ie_holidays = holidays.Ireland()
def is_ie_holiday(d):
    return d in ie_holidays

def working_day(d):
    if is_ie_holiday(d):
        return "Non Working Day"
    if d.weekday() < 5:
        return "Working Day"
    return "Non Working Day"

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--input",type=str)
argument_parser.add_argument("--usage-metric",type=int)
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

# use sklearn Lasso model to learn a function from inputs:
# "TIME ROUND 5m" as number of minutes (global_available_diff.index)
# "WORKDAY" boolean
# "DAY OF YEAR"
# "DAY OF YEAR"^2
# to output: "TOTAL AVAILABLE BIKES DIFF ABS"
# Step 1: subset training data by date < lib.PANDEMIC_START
# Step 2: create train-test split
# Step 3: Use 5-fold cross-validation (split train into 80% train and 20% val) to search for hyperparametr C of Lasso model
# Step 4: plot errorbars (mean score of 5 splits with std) for wide range of values of C
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split, TimeSeriesSplit
import matplotlib.pyplot as plt
from datetime import datetime

# Step 0: Assuming df_global_available_diff and lib.PANDEMIC_START are defined
# You may need to define lib.PANDEMIC_START as a specific date
pandemic_start = pd.to_datetime("2020-03-11")  # for example

# Step 1: Prepare the data with additional features
df_global_available_diff['TIME ROUND 5m'] = pd.to_datetime(df_global_available_diff['TIME ROUND 5m'])
df_global_available_diff['Timestamp'] = df_global_available_diff['TIME ROUND 5m'].apply(lambda x: x.timestamp())
df_global_available_diff['Workday'] = df_global_available_diff['TIME ROUND 5m'].dt.weekday < 5  # Monday=0, Sunday=6
df_global_available_diff["Workday (hols)"] = df_global_available_diff['TIME ROUND 5m'].map(lib.working_day) == 1
df_global_available_diff['Day of Year'] = df_global_available_diff['TIME ROUND 5m'].dt.dayofyear
df_global_available_diff['Day of Year Squared'] = np.square(df_global_available_diff['Day of Year'])

# Step 2: Subset the data by date
subset_df = df_global_available_diff[df_global_available_diff['TIME ROUND 5m'] < pandemic_start]

# Step 3: Train-test split
X = subset_df[['Timestamp', 'Workday', 'Workday (hols)', 'Day of Year', 'Day of Year Squared']]
y = subset_df['TOTAL AVAILABLE BIKES DIFF ABS'].fillna(0)
print(subset_df[subset_df["TOTAL AVAILABLE BIKES DIFF ABS"].isna()])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Cross-validation and hyperparameter tuning
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Parameters for Lasso
C = 1.1
alpha = 1/C

# Set up KFold with no shuffling
cv = KFold(n_splits=5, shuffle=False)

# Prepare lists to hold the MSE for each fold for the Lasso and baseline models
mse_folds_lasso = []
mse_folds_baseline1 = []
mse_folds_baseline2 = []
mse_folds_baseline3 = []

# Loop through each fold for cross-validation
for train_idx, test_idx in cv.split(X_train):
    # Splitting the data
    X_train_fold, X_test_fold = X_train.iloc[train_idx], X_train.iloc[test_idx]
    y_train_fold, y_test_fold = y_train.iloc[train_idx], y_train.iloc[test_idx]

    # Train and evaluate Lasso model for this fold
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train_fold, y_train_fold)
    y_pred_lasso = lasso.predict(X_test_fold)
    mse_folds_lasso.append(mean_squared_error(y_test_fold, y_pred_lasso))

    # Baseline Model 1: Always Predict Mean
    mean_value_fold = y_train_fold.mean()
    predictions_baseline1_fold = np.full(shape=y_test_fold.shape, fill_value=mean_value_fold)
    mse_folds_baseline1.append(mean_squared_error(y_test_fold, predictions_baseline1_fold))

    # Baseline Model 2: Predict Mean Based on Workday
    workday_mean_fold = y_train_fold[X_train_fold['Workday']].mean()
    non_workday_mean_fold = y_train_fold[~X_train_fold['Workday']].mean()
    predictions_baseline2_fold = X_test_fold['Workday'].apply(lambda x: workday_mean_fold if x else non_workday_mean_fold)
    mse_folds_baseline2.append(mean_squared_error(y_test_fold, predictions_baseline2_fold))

    # Baseline Model 3: Predict Mean Based on Workday (accounting for holidays)
    workday_mean_fold2 = y_train_fold[X_train_fold['Workday (hols)']].mean()
    non_workday_mean_fold2 = y_train_fold[~X_train_fold['Workday (hols)']].mean()
    predictions_baseline3_fold = X_test_fold['Workday (hols)'].apply(lambda x: workday_mean_fold2 if x else non_workday_mean_fold2)
    mse_folds_baseline3.append(mean_squared_error(y_test_fold, predictions_baseline3_fold))

# Calculate mean and standard deviation for MSE of each model
lasso_mse_mean = np.mean(mse_folds_lasso)
lasso_mse_std = np.std(mse_folds_lasso)
baseline1_mse_mean = np.mean(mse_folds_baseline1)
baseline1_mse_std = np.std(mse_folds_baseline1)
baseline2_mse_mean = np.mean(mse_folds_baseline2)
baseline2_mse_std = np.std(mse_folds_baseline2)
baseline3_mse_mean = np.mean(mse_folds_baseline3)
baseline3_mse_std = np.std(mse_folds_baseline3)

# Print results
print("Lasso Model - MSE Mean:", lasso_mse_mean, "MSE STD:", lasso_mse_std)
print("Baseline Mean Model - MSE Mean:", baseline1_mse_mean, "MSE STD:", baseline1_mse_std)
print("Baseline Workday Model - MSE Mean:", baseline2_mse_mean, "MSE STD:", baseline2_mse_std)
print("Baseline Workday (hols) Model - MSE Mean:", baseline3_mse_mean, "MSE STD:", baseline3_mse_std)

# Plotting the models' performances
plt.figure(figsize=(10, 6))

# Function to plot a horizontal line with shaded error region
x = 0
def plot_horizontal_line_with_shade(center, std_dev, label, color):
    global x
    plt.errorbar(x, center, yerr=std_dev, fmt='o',color=color, label=label, capsize=5)
    x = x+1

# Plotting Lasso model performance
plot_horizontal_line_with_shade(lasso_mse_mean, lasso_mse_std, 'Lasso Model', 'b')

# Plotting Baseline Model 1 performance with shaded error region
plot_horizontal_line_with_shade(baseline1_mse_mean, baseline1_mse_std, 'Baseline Mean Model', 'r')

# Plotting Baseline Model 2 performance with shaded error region
plot_horizontal_line_with_shade(baseline2_mse_mean, baseline2_mse_std, 'Baseline Workday Model', 'g')

# Plotting Baseline Model 2 performance with shaded error region
plot_horizontal_line_with_shade(baseline3_mse_mean, baseline3_mse_std, 'Baseline Workday (hols) Model', 'purple')

plt.legend()
plt.xlabel('Model')
plt.ylabel('Mean square error')
plt.title('Model Comparison with Cross-Validation Results')
plt.legend()
plt.tight_layout()
plt.savefig(directory + "/lasso_vs_baselines.pdf")
