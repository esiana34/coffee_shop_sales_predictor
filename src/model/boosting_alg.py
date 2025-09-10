import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt



file_path = (r"C:\Users\esian\Desktop\Kafe\src\model\merged_data.csv")
df = pd.read_csv(file_path)

# make the features (X) and the target (Y)

# Filter data for sandwiches
encoder = LabelEncoder()
df['item_encoded'] = encoder.fit_transform(df['item'])
# Features
X = df[['day_of_week', 'is_holiday','sales_lag_1', 'sales_lag_2', 'sales_lag_3', 'sales_lag_7','temperature_2m_max', 'temperature_2m_min', 'precipitation_sum','item_encoded']]  
y = df['sales'].fillna(0)

# checking shape 
print(X.shape, y.shape) 
# filling NAN as 0 to prevent error 
y = y.fillna(0) 

#splitting dataset 
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, train_size=0.8)

# prepare xgboost regressor
model = xgb.XGBRegressor(
    # no. of boostinf rounds
    n_estimators = 100, 
    # no. of considered in the tree
    learning_rate = 0.1,
    # max of each tree in depth
    max_depth = 4,
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

# Calculate average sales per item
average_sales = df.groupby('item')['sales'].mean()

# Print the averages
print("Average sales per item:")
print(average_sales)


xgb.plot_importance(model)
plt.show()