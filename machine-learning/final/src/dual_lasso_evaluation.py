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
feature_df = pd.DataFrame({
    "TIME ROUND 5m": global_available_diff.index,
    "TOTAL AVAILABLE BIKES": global_available.values,
    "TOTAL AVAILABLE BIKES DIFF ABS": global_available_diff.values
})
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
import matplotlib.pyplot as plt
from datetime import datetime
import lib
from sklearn.model_selection import KFold

# Step 1: Prepare the data with additional features
min_timestamp = df["TIME"].min().timestamp()
feature_df['TIME ROUND 5m'] = pd.to_datetime(feature_df['TIME ROUND 5m'])
feature_df["Workday (hols)"] = feature_df['TIME ROUND 5m'].map(lib.working_day)
feature_df['Minutes'] = feature_df['TIME ROUND 5m'].apply(lambda x: x.timestamp() - min_timestamp)
feature_df['Workday'] = feature_df['TIME ROUND 5m'].dt.weekday < 5  # Monday=0, Sunday=6
feature_df['Day of Year'] = feature_df['TIME ROUND 5m'].dt.dayofyear
feature_df['Day of Year Squared'] = np.square(feature_df['Day of Year'])

feature_df['Interval'] = feature_df['TIME ROUND 5m'].dt.hour * 2 + feature_df['TIME ROUND 5m'].dt.minute // 30
intervals_one_hot = pd.get_dummies(feature_df['Interval'], prefix='Interval')
feature_df = pd.concat([feature_df, intervals_one_hot], axis=1)

from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold, GridSearchCV

feature_df = feature_df.set_index(feature_df["TIME ROUND 5m"])
features = ["Minutes", "Workday (hols)"] + [col for col in feature_df.columns if col.startswith("Interval")]
X = feature_df[features]
y = feature_df["TOTAL AVAILABLE BIKES DIFF ABS"].fillna(0)

X_pre_pandemic = X[X.index < lib.PANDEMIC_START]
y_pre_pandemic = y[y.index < lib.PANDEMIC_START]
#X = X.set_index(df_global_available_diff["TIME ROUND 5m"])
#y = y.set_index()
cv = KFold(n_splits=5,shuffle=False)

# Plot
plt.figure(figsize=(8, 3))
colors = ['red', 'blue', 'green', 'purple', 'orange']  # Colors for different splits
split_labels = [f"Split {i+1}" for i in range(5)]  # Labels for different splits
for i, (train_index, test_index) in enumerate(cv.split(y_pre_pandemic)):
    plt.scatter(y_pre_pandemic.index[test_index], y_pre_pandemic.iloc[test_index], c=colors[i], label=split_labels[i],s=0.5)
plt.title('KFold Splits on Pre-Pandemic Data')
plt.xlabel('Time')
plt.ylabel('Pseudousage')
plt.legend()
plt.tight_layout()
plt.savefig(directory + "/pre-pandemic-cross-val-split.pdf")



def train_lasso_dual(X_train,y_train):
    # Subset 1: Where "Workday (hols)" = True
    X_workday = X_train[X_train['Workday (hols)'] == 1]
    y_workday = y_train[X_train['Workday (hols)'] == 1]

    # Best model for Workday
    workday_alpha = 1/100
    non_workday_alpha = 1/100
    model_workday = Lasso(alpha=workday_alpha)
    model_workday.fit(X_workday, y_workday)

    # Subset 2: Where "Workday (hols)" = False
    X_non_workday = X_train[X_train['Workday (hols)'] == 0]
    y_non_workday = y_train[X_train['Workday (hols)'] == 0]

    # Best model for Non-Workday
    model_non_workday = Lasso(alpha=non_workday_alpha)
    model_non_workday.fit(X_non_workday, y_non_workday)

    return model_workday, model_non_workday

def dual_model_predict(X,y,model_workday, model_non_workday):
    workday_filter = X['Workday (hols)'] == 1
    non_workday_filter = X['Workday (hols)'] == 0
    y_pred = np.zeros_like(y)
    y_pred[workday_filter] = model_workday.predict(X[workday_filter])
    y_pred[non_workday_filter] = model_non_workday.predict(X[non_workday_filter])
    return y_pred

def evaluate_dual_model(X, y, model_workday, model_non_workday):
    y_pred = dual_model_predict(X,y,model_workday,model_non_workday)
    y_day = y.groupby(y.index.date).sum()
    y_pred = pd.Series(y_pred,name="PRED",index=y.index)
    y_pred_day = y_pred.groupby(y_pred.index.date).sum()
    mse = mean_squared_error(y, y_pred)
    day_mse = mean_squared_error(y_day,y_pred_day)
    print("day mse:", day_mse)
    return mse, day_mse

def predict_baseline(X,y,X_train,y_train):
    workday_mean = y_train[X_train['Workday (hols)'] == 1].mean()
    non_workday_mean = y_train[~(X_train['Workday (hols)'] == 1)].mean()
    predictions = X['Workday (hols)'].apply(lambda x: workday_mean if x else non_workday_mean)
    return predictions

def evaluate_baseline(X,y,X_train,y_train):
    workday_mean = y_train[X_train['Workday (hols)'] == 1].mean()
    non_workday_mean = y_train[~(X_train['Workday (hols)'] == 1)].mean()
    predictions = X['Workday (hols)'].apply(lambda x: workday_mean if x else non_workday_mean)
    predictions_day = predictions.groupby(predictions.index.date).sum()
    true_day = y.groupby(y.index.date).sum()
    mse = mean_squared_error(y, predictions)
    mse_day = mean_squared_error(true_day, predictions_day)
    return mse, mse_day

# mse_test_dual_model = lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday)
# mse_baseline = lib.evaluate_baseline(X_test,y_test,X_train,y_train)

# print("dual model mse:", mse_test_dual_model)
# print("baseline model mse:", mse_baseline)

# print("dual model mse day:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='d')))
# print("baseline model mse day:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='d')))

# print("dual model mse week:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='w')))
# print("baseline model mse week:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='w')))

# print("dual model mse month:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='M')))
# print("baseline model mse month:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='M')))



dual_day_mse = []
base_day_mse = []
dual_time_mse = []
base_time_mse = []
dual_week_mse = []
base_week_mse = []
dual_month_mse = []
base_month_mse = []

# Firstly evaluate the models on pre pandemic data only
print(X_pre_pandemic.index)
for train_index, test_index in cv.split(X_pre_pandemic):
    X_train = X_pre_pandemic.iloc[train_index]
    y_train = y_pre_pandemic.iloc[train_index]
    X_test = X_pre_pandemic.iloc[test_index]
    y_test = y_pre_pandemic.iloc[test_index]

    model_workday, model_non_workday = train_lasso_dual(X_train,y_train)
    
    # mse_dual = evaluate_dual_model(X_test, y_test,model_workday,model_non_workday)
    # mse_baseline = evaluate_baseline(X_test,y_test,X_train,y_train)

    dual_time_mse.append(lib.evaluate_dual_model(X_test,y_test,model_workday, model_non_workday))
    base_time_mse.append(lib.evaluate_baseline(X_test,y_test,X_train,y_train))

    
    dual_day_mse.append(lib.evaluate_dual_model(X_test,y_test,model_workday, model_non_workday,pd.Grouper(freq='d')))
    base_day_mse.append(lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='d')))

    dual_week_mse.append(lib.evaluate_dual_model(X_test,y_test,model_workday,model_non_workday,pd.Grouper(freq='w')))
    base_week_mse.append(lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='w')))

    dual_month_mse.append(lib.evaluate_dual_model(X_test,y_test,model_workday,model_non_workday,pd.Grouper(freq='M')))
    base_month_mse.append(lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='M')))

    # mse_test_dual_model = lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday)
    # mse_baseline = lib.evaluate_baseline(X_test,y_test,X_train,y_train)

    # print("dual model mse:", mse_test_dual_model)
    # print("baseline model mse:", mse_baseline)

    # print("dual model mse day:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='d')))
    # print("baseline model mse day:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='d')))

    # print("dual model mse week:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='w')))
    # print("baseline model mse week:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='w')))

    # print("dual model mse month:",lib.evaluate_dual_model(X_test, y_test, model_workday, model_non_workday,pd.Grouper(freq='M')))
    # print("baseline model mse month:", lib.evaluate_baseline(X_test,y_test,X_train,y_train,pd.Grouper(freq='M')))

results = pd.DataFrame({
    "mse on time dual lasso": dual_time_mse,
    "mse on time baseline": base_time_mse,
    "mse on day dual lasso": dual_day_mse,
    "mse on day baseline": base_day_mse,
    "mse on week dual lasso": dual_week_mse,
    "mse on week baseline": base_week_mse,
    "mse on month dual lasso": dual_month_mse,
    "mse on month baseline": base_month_mse,
})

results.to_csv(directory + "/dual_lasso_eval.csv")
print(results)
print(results.describe())

model_workday, model_non_workday = train_lasso_dual(X_pre_pandemic,y_pre_pandemic)

y_all_pred = dual_model_predict(X,y,model_workday,model_non_workday)
pd.DataFrame({
    "true": y,
    "pred": y_all_pred,
}).to_csv(directory + "/prediction_all_dual_lasso.csv")


y_all_pred = predict_baseline(X,y,X_pre_pandemic,y_pre_pandemic)
pd.DataFrame({
    "true": y,
    "pred": y_all_pred,
}).to_csv(directory + "/prediction_all_baseline.csv")