import pandas as pd

df_v4 = pd.read_csv("/mnt/data/skunkworks_data_v4.csv")

total_donations_zip = df_v4.groupby('Zip')['Amount'].sum().reset_index(name='Total Donations')

average_donation_overall = df_v4['Amount'].mean()

average_donation_campaign = df_v4.groupby('Campaign')['Amount'].mean().reset_index(name='Average Donation')

average_donation_donor_type = df_v4.groupby('Type')['Amount'].mean().reset_index(name='Average Donation')

df_v4['Total Donations per Zip'] = df_v4['Zip'].map(total_donations_zip.set_index('Zip')['Total Donations'])

df_v4['Average Donation per Campaign'] = df_v4['Campaign'].map(average_donation_campaign.set_index('Campaign')['Average Donation'])

df_v4['Average Donation per Donor Type'] = df_v4['Type'].map(average_donation_donor_type.set_index('Type')['Average Donation'])

new_file_path = "/mnt/data/skunkworks_data_v5.csv"
df_v4.to_csv(new_file_path, index=False)
