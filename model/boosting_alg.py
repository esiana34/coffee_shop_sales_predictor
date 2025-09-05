# gradient boosting and decision trees
import xgboost as xgb
import pandas as pd
# from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

import matplotlib.pyplot as plt


# open sample data fiel
file_path = (r"C:\Users\esian\Desktop\Kafe\data\prove\samples.csv")
df = pd.read_csv(file_path)

# make the features (X) and the target (Y)

# Filter data for sandwiches
sandwich_df = df[df['item'].str.lower() == 'sandwich']

# Features
X = sandwich_df[['day_of_week', 'is_holiday']]  

# Target
y = sandwich_df['sales']  

print(X.shape, y.shape)  # should match
y = y.fillna(0)  # replace NaN with 0

#splitting dataset 
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, train_size=0.8)

# prepare xgboost model

model = xgb.XGBRegressor(
    # no. of boostinf rounds
    n_estimators = 100, 
    # no. of considered in the tree
    learning_rate = 0.1,
    # max of each tree in depth
    max_depth = 3,
    random_state= 42
)

# train model
model.fit(X_train, y_train)

# predict
y_predict= model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_predict)
print("Mean Squared Error:", mse)

mae = mean_absolute_error(y_test, y_predict)
print(f"Mean Absolute Error:", mae)


new_data = pd.DataFrame({"day_of_week": [4], "is_holiday": [1]})
print("Predicted sandwiches:", model.predict(new_data)[0])

xgb.plot_importance(model)
plt.show()