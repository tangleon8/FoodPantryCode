import pandas as pd

data_path = '/Users/leontang/Downloads/Skunkworks_Theriver_raw_v2.xlsx'
data = pd.read_excel(data_path)
data.head()

data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month


data_2023 = data[data['Year'] == 2023]
data_2024 = data[data['Year'] == 2024]

summary_2023 = data_2023.groupby('Month').agg(Total_Donated=('Amount', 'sum'), Donation_Count=('Amount', 'count'))
summary_2024 = data_2024.groupby('Month').agg(Total_Donated=('Amount', 'sum'), Donation_Count=('Amount', 'count'))

print("Donation summary for 2023:")
print(summary_2023)
print("\nDonation summary for 2024:")
print(summary_2024)
