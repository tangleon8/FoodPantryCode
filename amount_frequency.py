import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.hist(data['Amount'], bins=50, color='blue', edgecolor='black', alpha=0.7)
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
