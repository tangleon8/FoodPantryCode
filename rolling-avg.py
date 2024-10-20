import matplotlib.pyplot as plt

plt.figure(figsize=(15, 6))

plt.plot(data.index, data['rolling_sum_3day'], label='3-Day Rolling Sum', alpha=0.7)
plt.plot(data.index, data['rolling_sum_5day'], label='5-Day Rolling Sum', alpha=0.7)
plt.plot(data.index, data['rolling_sum_7day'], label='7-Day Rolling Sum', alpha=0.7)

plt.title('Rolling Sum of Donations Over Time')
plt.xlabel('Date')
plt.ylabel('Donation Sum')
plt.legend(loc='upper left')
plt.grid(True)

plt.show()

plt.figure(figsize=(15, 6))

plt.plot(data.index, data['rolling_avg_3day'], label='3-Day Rolling Avg', alpha=0.7)
plt.plot(data.index, data['rolling_avg_5day'], label='5-Day Rolling Avg', alpha=0.7)
plt.plot(data.index, data['rolling_avg_7day'], label='7-Day Rolling Avg', alpha=0.7)

plt.title('Rolling Average of Donations Over Time')
plt.xlabel('Date')
plt.ylabel('Donation Average')
plt.legend(loc='upper left')
plt.grid(True)

plt.show()
