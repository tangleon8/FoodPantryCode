import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score

file_path = '/Users/leontang/Downloads/Skunkworks_Theriver_raw_v2.xlsx'
data_df = pd.read_excel(file_path, sheet_name='Data')

missing_values = data_df.isnull().sum()
duplicates = data_df.duplicated().sum()

cleaned_data_df = data_df.drop_duplicates()

print("Missing Values:\n", missing_values)
print("\nNumber of Duplicates:", duplicates)

print("\nData shape after removing duplicates:", cleaned_data_df.shape)

scaler = StandardScaler()
cleaned_data_df['Amount'] = scaler.fit_transform(cleaned_data_df[['Amount']])

categorical_columns = ['Type', 'Fund', 'Campaign', 'Appeal']
encoded_data_df = pd.get_dummies(cleaned_data_df, columns=categorical_columns, drop_first=True)

print("\nTransformed Data (first 5 rows):\n", encoded_data_df.head())
