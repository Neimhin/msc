import pandas as pd
import numpy as np
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
from sklearn.linear_model import Ridge 
import numpy as np
custom_model = Ridge()
custom_model.intercept_ = -11.02
custom_model.coef_ = np.array([-0.76, -0.2, 0.49, 1.22, 2.8, -0.51, 0.15])
predicted_points = custom_model.predict(x_test)
predicted_superior = predicted_points > 0
print(np.mean(np.abs(predicted_points - y_test)))
print(accuracy_score(predicted_superior, y_sup_test)) # 0.782
