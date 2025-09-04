# gradient boosting and decision trees
import xgboost as xgb
import pandas as pd
# from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# open sample data fiel
file_path = (r"C:\Users\esian\Desktop\Kafe\data\prove\samples.csv")
df = pd.read_csv(file_path)

# make the features (X) and the target (Y)

# Filter data for sandwiches
sandwich_df = df[df['item'].str.lower() == 'sandwich']

# Features
X = sandwich_df[['day_of_week', 'is_weekend']]  # only sandwich rows

# Target
y = sandwich_df['sales']  # only sandwich rows

print(X.shape, y.shape)  # should match
y = y.fillna(0)  # replace NaN with 0

#splitting dataset 
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, train_size=0.8, shuffle=True)

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


new_data = pd.DataFrame({"day_of_week": [4], "is_weekend": [0]})
print("Predicted sandwiches:", model.predict(new_data)[0])
