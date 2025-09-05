import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

from keras import Sequential
from keras import layers
from keras.layers import Dense


# Load data (example with sandwiches)
file_path = (r"C:\Users\esian\Desktop\Kafe\data\prove\samples.csv")
df = pd.read_csv(file_path)

item_df = df[df['item'].str.lower() == 'sandwich']

X = item_df[['day_of_week', 'is_weekend', 'is_holiday']]
y = item_df['sales'].fillna(0)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, train_size=0.8, random_state=42, shuffle=True)

# Build neural network
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1))  # Output layer for regression

# Compile and train
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=16, verbose=1)

# Predict and evaluate
y_pred = model.predict(X_test)

# Predict and evaluate
y_pred = model.predict(X_test)

# Show a few predictions vs. actual values
for i in range(5):  # show first 5 examples
    print(f"Predicted: {y_pred[i][0]:.2f}, Actual: {y_test.iloc[i]:.2f}")

# Optionally compute error metrics
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Performance:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")
