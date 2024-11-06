import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import shap
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/leontang/Downloads/skunkworks_data_v5_full.csv')

data['Date'] = pd.to_datetime(data['Date'])

# Encode categorical columns except for 'Appeal'
categorical_columns = data.select_dtypes(include=['object']).columns.difference(['Appeal'])
label_encoders = {col: LabelEncoder().fit(data[col]) for col in categorical_columns}

for col, le in label_encoders.items():
    data[col] = le.transform(data[col])

# Iterate over each unique appeal type to perform SHAP analysis
for appeal_type in data['Appeal'].unique():
    print(f"SHAP Analysis for Appeal Type: {appeal_type}")
    
    # Filter data for the specific appeal type
    appeal_data = data[data['Appeal'] == appeal_type]
    
    # Define the target and feature set (dropping 'Date' and keeping 'Appeal' as is)
    X = appeal_data.drop(columns=["Amount", "Date"])
    y = appeal_data["Amount"]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a RandomForest model
    model = RandomForestRegressor(n_estimators=20, random_state=42) 
    model.fit(X_train, y_train)
    
    #  SHAP explainer and usse a smaller sample for faster analysis
    explainer = shap.TreeExplainer(model)
    sample_X_train = X_train.sample(n=1000, random_state=42) if len(X_train) > 1000 else X_train  
    sample_shap_values = explainer.shap_values(sample_X_train)
    
    # Plot SHAP values for the current appeal type
    shap.summary_plot(sample_shap_values, sample_X_train, plot_type="bar", show=False)
    plt.title(f"Feature Importance for Appeal Type: {appeal_type}")
    plt.show()
    
    shap.summary_plot(sample_shap_values, sample_X_train, show=False)
    plt.title(f"Detailed Feature Impact for Appeal Type: {appeal_type}")
    plt.show()
