import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import Ridge 
from sklearn.metrics import accuracy_score

# Read the data
df = pd.read_csv("wine_review.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Prepare the data
x = df[["price", "Soft", "Crisp", "Full", "Rich"]]
drop = [
        "price",
        # "Soft",
        # "Crisp",
        # "Full",
        # "Rich",
        ]
# x["not_rich"] = ~x["Rich"]
# x["not_full"] = ~x["Full"]
# x["not_soft"] = ~x["Soft"]
# x["not_crisp"] = ~x["Crisp"]
x["log(price)"] = np.log(x["price"])
x["rich_and_full"] = x["Rich"] * x["Full"]
# # x["not_soft_and_rich"] = x["not_soft"] * x["Rich"]
x["soft_and_crisp"] = x["Soft"] * x["Crisp"]
# x["rich_and_log_price"] = x["Rich"] * x["log(price)"]
x = x.drop(columns=drop)
y = df["points"] - 90
y_sup = df["superior_rating"]

x_test = x[2000:]
x = x[:2000]
y_test = y[2000:]
y = y[:2000]
y_sup_test = y_sup[2000:]
y_sup = y_sup[:2000]

# Set up cross-validation
splitter = StratifiedKFold(n_splits=5)

# Define the model
model = Ridge(fit_intercept=True)

# Define the hyperparameters grid

param_grid = {'alpha': np.logspace(start=-100, stop=-4, num=40)}

# Perform grid search
grid_search = GridSearchCV(model, param_grid, cv=splitter, scoring='neg_mean_absolute_error')
grid_search.fit(x, y)

# Plot the mean and std of accuracy against the l2 hyperparameter C
means = grid_search.cv_results_['mean_test_score']
stds = grid_search.cv_results_['std_test_score']
params = grid_search.cv_results_['param_alpha']

best_val_score_i = np.argmax(means)
best_C = params[best_val_score_i]
print(best_val_score_i)

# Plot ROC curve
fix, ax = plt.subplots(nrows=2, ncols=1)
ax[0].errorbar(params, means, yerr=stds, fmt='o')
ax[0].axhline(np.max(means), color='red', label=f"$C={best_C}$")
ax[0].set_xlabel('C (Regularization parameter)')
ax[0].set_ylabel('Accuracy')
ax[0].set_title('Mean and std of Accuracy vs C')
ax[0].set_xscale('log')
ax[0].legend()

# Print the best hyperparameters
print("Best hyperparameters:", grid_search.best_params_)
# Print the best cross-validation score (accuracy)
print("Best cross-validation score (neg_mean_absolute_error):", grid_search.best_score_)

# Evaluate the best model on the entire dataset


best_model = grid_search.best_estimator_
feature_names = ["intercept"] + x.columns.tolist()
coefficients = [best_model.intercept_] +  list(best_model.coef_)

print(best_model.intercept_, best_model.coef_)
print(feature_names)
print(coefficients)
coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})
print(coef_df)

predicted_points = best_model.predict(x_test)
predicted_superior = predicted_points > 0
print((predicted_superior == (y_sup_test == 1)).mean())

from sklearn.linear_model import Ridge 
import numpy as np
custom_model = Ridge()
custom_model.intercept_ = -11.02
custom_model.coef_ = np.array([-0.76, -0.2, 0.49, 1.22, 2.8, -0.51, 0.15])
predicted_points = custom_model.predict(x_test)
predicted_superior = predicted_points > 0
print(np.mean(np.abs(predicted_points - y_test)))
print((predicted_superior == (y_sup_test == 1)).mean())
