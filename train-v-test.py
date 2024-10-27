import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

file_path = '/leontang8/data/skunkworks_data_v4.csv'
data = pd.read_csv(file_path)


label_encoders = {}
categorical_columns = ['Type', 'Fund', 'Campaign', 'Appeal']

for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    data[col] = label_encoders[col].fit_transform(data[col])

X = data.drop(columns=['Amount', 'Date', 'Account Number', 'Zip'])
y = data['Amount']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

train_predictions = model.predict(X_train)

plt.figure(figsize=(10, 6))
plt.scatter(y_train, train_predictions, edgecolors=(0, 0, 0), alpha=0.5)
plt.plot([y_train.min(), 140], [y_train.min(), 140], 'r--', lw=2)
plt.xlim(0, 140)
plt.ylim(0, 140)
plt.title('Actual vs Predicted Training Amounts (Training Set)')
plt.xlabel('Actual Donation Amount')
plt.ylabel('Predicted Donation Amount')
plt.grid(True)
plt.show()

test_predictions = model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_test, test_predictions, edgecolors=(0, 0, 0), alpha=0.5)
plt.plot([y_test.min(), 120], [y_test.min(), 120], 'r--', lw=2)
plt.xlim(0, 120)
plt.ylim(0, 120)
plt.title('Actual vs Predicted Testing Amounts (Test Set)')
plt.xlabel('Actual Donation Amount')
plt.ylabel('Predicted Donation Amount')
plt.grid(True)
plt.show()
