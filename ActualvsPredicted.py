#Training Data 

from sklearn.model_selection import train_test_split

# Split the data into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model on the training set
model.fit(X_train, y_train)

# Get predictions on the training set
train_predictions = model.predict(X_train)

# Plot actual vs predicted for training data
plt.figure(figsize=(10,6))
plt.scatter(y_train, train_predictions, edgecolors=(0, 0, 0), alpha=0.5)
plt.plot([y_train.min(), 140], [y_train.min(), 140], 'r--', lw=2)
plt.xlim(0, 140)
plt.ylim(0, 140)
plt.title('Actual vs Predicted Training Amounts (Training Set)')
plt.xlabel('Actual Donation Amount')
plt.ylabel('Predicted Donation Amount')
plt.grid(True)
plt.show()


#Testing Data
# Get predictions on the testing set
test_predictions = model.predict(X_test)

# Plot actual vs predicted for testing data
plt.figure(figsize=(10,6))
plt.scatter(y_test, test_predictions, edgecolors=(0, 0, 0), alpha=0.5)
plt.plot([y_test.min(), 120], [y_test.min(), 120], 'r--', lw=2)
plt.xlim(0, 120)
plt.ylim(0, 120)
plt.title('Actual vs Predicted Testing Amounts (Test Set)')
plt.xlabel('Actual Donation Amount')
plt.ylabel('Predicted Donation Amount')
plt.grid(True)
plt.show()
