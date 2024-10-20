import seaborn as sns

plt.figure(figsize=(10, 8))
plt.title('Feature Correlation Heatmap')

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.show()
