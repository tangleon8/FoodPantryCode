import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

data = pd.read_csv('/Users/leontang/Downloads/Skunkworks_Theriver_raw_v1.xlsx - Data.csv')



#print(data.info())


#print(data.head())

#print(data.describe())

#print(data.isnull().sum())

#Cleans the data and converts to float
data['Amount'] = data['Amount'].replace({'\$': '', ',': ''}, regex=True).astype(float)

#Defines the list of columns
categorical_columns = ['Type', 'Fund', 'Campaign', 'Appeal']

#Converts the categorical columns into dummy variables
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

#Makes a new binary column to find repeat donations from Account Number
data['Donated_Again'] = data.duplicated(subset=['Account Number'], keep=False).astype(int)

#Drops the unnessaracy stuff
data = data.drop(columns=['Date', 'Primary ZIP Code', 'Account Number'])

#What is x and y
X = data.drop('Donated_Again', axis=1)
y = data['Donated_Again']

#Training vs testing sets with 30% of data used for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Trains a RandomForestClassifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

#Predict the test set results and prints the output of the SVMs
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
