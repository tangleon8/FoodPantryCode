import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar

years = data['Date'].dt.year.unique()
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=f'{min(years)}-01-01', end=f'{max(years)}-12-31')

non_federal_holidays = {
    'Valentine\'s Day': pd.date_range(start=f'{min(years)}-02-14', end=f'{max(years)}-02-14', freq='A'),
    'Halloween': pd.date_range(start=f'{min(years)}-10-31', end=f'{max(years)}-10-31', freq='A')
}
for holiday, dates in non_federal_holidays.items():
    holidays = holidays.append(dates)

def calculate_proximity_to_holidays(df, holiday_dates):
    # Convert holiday dates to a DataFrame for merging
    holiday_df = pd.DataFrame({'Holiday': holiday_dates})
    holiday_df['Key'] = 0

    df['Key'] = 0
    df = df.merge(holiday_df, on='Key').drop('Key', 1)
    
    df['Days_to_Holiday'] = (df['Holiday'] - df['Date']).dt.days
    
    df_upcoming = df[df['Days_to_Holiday'] >= 0].groupby('Date')['Days_to_Holiday'].min().reset_index()
    df_upcoming.columns = ['Date', 'Days_to_Next_Holiday']
    
    df_past = df[df['Days_to_Holiday'] <= 0].groupby('Date')['Days_to_Holiday'].max().reset_index()
    df_past.columns = ['Date', 'Days_from_Previous_Holiday']

    df = df.merge(df_upcoming, on='Date', how='left')
    df = df.merge(df_past, on='Date', how='left')
    
    df = df.drop_duplicates(subset=['Date', 'Type', 'Fund', 'Campaign', 'Appeal', 'Zip', 'Account Number'])
    
    return df

data = calculate_proximity_to_holidays(data, holidays)
data[['Date', 'Days_to_Next_Holiday', 'Days_from_Previous_Holiday']].head()
