heatmap_data = data.groupby(['DayOfWeek', 'Season']).size().unstack()

day_labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
season_labels = ['Winter', 'Spring', 'Summer', 'Autumn']
heatmap_data.index = day_labels
heatmap_data.columns = season_labels

plt.figure(figsize=(10, 7))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)
plt.title('Donation Activity by Day of the Week and Season')
plt.xlabel('Season')
plt.ylabel('Day of the Week')
plt.show()
