import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
plt.scatter(y_test_5, predictions_rf_5_simplified, alpha=0.5)
plt.title('Actual vs Predicted - 5-Day Count')
plt.xlabel('Actual Counts')
plt.ylabel('Predicted Counts')
plt.plot([y_test_5.min(), y_test_5.max()], [y_test_5.min(), y_test_5.max()], 'k--', lw=2)  # Line for perfect predictions

plt.subplot(1, 2, 2)
plt.scatter(y_test_7, predictions_rf_7_simplified, alpha=0.5)
plt.title('Actual vs Predicted - 7-Day Count')
plt.xlabel('Actual Counts')
plt.ylabel('Predicted Counts')
plt.plot([y_test_7.min(), y_test_7.max()], [y_test_7.min(), y_test_7.max()], 'k--', lw=2)  # Line for perfect predictions

plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
plt.scatter(y_test_5, predictions_rf_5_simplified, alpha=0.5)
plt.title('Actual vs Predicted - 5-Day Count')
plt.xlabel('Actual Counts')
plt.ylabel('Predicted Counts')
plt.plot([y_test_5.min(), y_test_5.max()], [y_test_5.min(), y_test_5.max()], 'k--', lw=2)  # Line for perfect predictions

plt.subplot(1, 2, 2)
plt.scatter(y_test_7, predictions_rf_7_simplified, alpha=0.5)
plt.title('Actual vs Predicted - 7-Day Count')
plt.xlabel('Actual Counts')
plt.ylabel('Predicted Counts')
plt.plot([y_test_7.min(), y_test_7.max()], [y_test_7.min(), y_test_7.max()], 'k--', lw=2)  # Line for perfect predictions

plt.tight_layout()
plt.show()



