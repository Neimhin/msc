import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LinearRegression

# Read the data
df = pd.read_csv("wine_review.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Prepare the data
x = df[["price"]]
x["log(price)"] = np.log(x["price"])
x = x[["log(price)"]]
y = df["points"]

# Split the data into training and test sets
x_train_val = x[:2000] 
y_train_val = y[:2000]
x_test = x[2000:]
y_test = y[2000:]

# Set up cross-validation
splitter = StratifiedKFold(n_splits=5)

# Define the model
model = LinearRegression()

# Define the hyperparameters grid
param_grid = {'fit_intercept': [True, False]}

# Perform grid search
grid_search = GridSearchCV(model, param_grid, cv=splitter, scoring='r2')
grid_search.fit(x_train_val, y_train_val)

# Print the best hyperparameters
print("Best hyperparameters:", grid_search.best_params_)

# Print the best cross-validation score
print("Best cross-validation score (R^2):", grid_search.best_score_)

# Evaluate the model on the test set
test_score = grid_search.score(x_test, y_test)
print("Test set score (R^2):", test_score)


# Get the best model from grid search
best_model = grid_search.best_estimator_

# Predict points on the test set
print(best_model.intercept_)
print(best_model.coef_)
predicted_points = best_model.predict(x_test)
print(x_test.loc[2000], y_test.loc[2000], predicted_points[0])

# Convert predicted points into superior_rating predictions
predicted_superior_rating = (predicted_points > 90).astype(int)

# Calculate accuracy
accuracy = (predicted_superior_rating == y_test).mean()

# Print accuracy
print("Accuracy:", accuracy)

