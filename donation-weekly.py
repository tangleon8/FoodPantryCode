plt.figure(figsize=(8, 6))
sns.countplot(x='DayOfWeek', data=data)
plt.title('Distribution of Donations by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Donations')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
plt.show()
