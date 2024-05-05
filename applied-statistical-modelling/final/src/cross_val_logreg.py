import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
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
# x["not_soft_and_rich"] = x["not_soft"] * x["Rich"]
x["soft_and_crisp"] = x["Soft"] * x["Crisp"]
# x["rich_and_log_price"] = x["Rich"] * x["log(price)"]
x = x.drop(columns=drop)
y = df["superior_rating"]

x_test = x[2000:]
x = x[:2000]
y_test = y[2000:]
y = y[:2000]

# Set up cross-validation
splitter = StratifiedKFold(n_splits=5)

# Define the model
model = LogisticRegression(max_iter=10000)

# Define the hyperparameters grid

param_grid = {'C': np.logspace(start=-3, stop=2, num=40)}

# Perform grid search
grid_search = GridSearchCV(model, param_grid, cv=splitter, scoring='accuracy')
grid_search.fit(x, y)

# Plot the mean and std of accuracy against the l2 hyperparameter C
means = grid_search.cv_results_['mean_test_score']
stds = grid_search.cv_results_['std_test_score']
params = grid_search.cv_results_['param_C']

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
print("Best cross-validation score (Accuracy):", grid_search.best_score_)

# Evaluate the best model on the entire dataset


best_model = grid_search.best_estimator_
print(best_model.intercept_, best_model.coef_)

feature_names = x.columns.tolist()
coefficients = np.concatenate((best_model.intercept_, best_model.coef_[0]))
coef_df = pd.DataFrame({'Feature': ['Intercept'] + feature_names, 'Coefficient': coefficients})
print(coef_df)

predicted_superior_rating = best_model.predict(x_test)
accuracy = accuracy_score(y_test, predicted_superior_rating)
print("Accuracy on the test dataset:", accuracy)

predicted_superior_rating = best_model.predict(x)
accuracy = accuracy_score(y, predicted_superior_rating)
print("Accuracy on the train dataset:", accuracy)

from sklearn.metrics import roc_curve, auc

# Get predicted probabilities for positive class
predicted_probabilities = best_model.predict_proba(x)[:, 1]

# Compute ROC curve and ROC area for each class
fpr, tpr, _ = roc_curve(y, predicted_probabilities)
roc_auc = auc(fpr, tpr)

ax[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
ax[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
ax[1].set_xlabel('False Positive Rate')
ax[1].set_ylabel('True Positive Rate')
ax[1].set_title('Receiver Operating Characteristic (ROC)')
ax[1].legend(loc="lower right")

plt.savefig("fig/cross_val_logreg.pdf")
# Print AUC
print("AUC:", roc_auc)
