import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

data_path = '/Users/leontang/Downloads/skunkworks_data_v6.csv'  # Ensure this file path is correct and accessible
data = pd.read_csv(data_path)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Clean ZIP codes
data['Zip'] = data['Zip'].astype(str).str.replace(',', '').str.strip()

# Map numeric or coded seasons to actual season names
season_mapping = {
    1: 'Winter',  # Adjust based on your data's actual season codes
    2: 'Spring',
    3: 'Summer',
    4: 'Fall'
}
data['Season'] = data['Season'].map(season_mapping)

# Filter data to only include Wisconsin ZIP codes (assuming they start with "53")
wisconsin_data = data[data['Zip'].str.startswith('53')]

# Streamlit app layout
st.set_page_config(page_title="Interactive Donation Dashboard", layout="wide")
st.title("Interactive Donation Data Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")

# Date range selection
selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    [data['Date'].min(), data['Date'].max()]
)

# Dual-list multiselect for Type
all_types = list(data['Type'].unique())
selected_type = st.sidebar.multiselect("Selected Types", all_types, default=all_types)
available_types = [t for t in all_types if t not in selected_type]

st.sidebar.subheader("Available Types")
selected_to_add = st.sidebar.multiselect("Add Types", available_types)
if selected_to_add:
    selected_type.extend(selected_to_add)
    available_types = [t for t in all_types if t not in selected_type]

# Dual-list multiselect for Campaign
all_campaigns = list(data['Campaign'].unique())
selected_campaign = st.sidebar.multiselect("Selected Campaigns", all_campaigns, default=all_campaigns)
available_campaigns = [c for c in all_campaigns if c not in selected_campaign]

st.sidebar.subheader("Available Campaigns")
selected_campaign_to_add = st.sidebar.multiselect("Add Campaigns", available_campaigns)
if selected_campaign_to_add:
    selected_campaign.extend(selected_campaign_to_add)
    available_campaigns = [c for c in all_campaigns if c not in selected_campaign]

# Dual-list multiselect for ZIP code (Wisconsin only)
all_zips = list(wisconsin_data['Zip'].unique())
selected_zip = st.sidebar.multiselect("Selected ZIP Codes", all_zips, default=all_zips)
available_zips = [z for z in all_zips if z not in selected_zip]

st.sidebar.subheader("Available ZIP Codes")
selected_zip_to_add = st.sidebar.multiselect("Add ZIP Codes", available_zips)
if selected_zip_to_add:
    selected_zip.extend(selected_zip_to_add)
    available_zips = [z for z in all_zips if z not in selected_zip]

# Donation amount sliders
min_donation = st.sidebar.slider("Minimum Donation Amount", min_value=float(data['Amount'].min()), max_value=float(data['Amount'].max()), value=float(data['Amount'].min()))
max_donation = st.sidebar.slider("Maximum Donation Amount", min_value=float(data['Amount'].min()), max_value=float(data['Amount'].max()), value=float(data['Amount'].max()))

# Apply filters
filtered_data = data[
    (data['Date'] >= pd.to_datetime(selected_date_range[0])) &
    (data['Date'] <= pd.to_datetime(selected_date_range[1])) &
    (data['Type'].isin(selected_type)) &
    (data['Campaign'].isin(selected_campaign)) &
    (data['Zip'].isin(selected_zip)) &
    (data['Amount'] >= min_donation) &
    (data['Amount'] <= max_donation)
]

# Display filtered data overview
st.subheader("Filtered Data Overview")
st.dataframe(filtered_data)

# Dynamic summary metrics
st.subheader("Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Donations", f"${filtered_data['Amount'].sum():,.2f}")
with col2:
    st.metric("Average Donation", f"${filtered_data['Amount'].mean():,.2f}")
with col3:
    st.metric("Number of Donations", f"{filtered_data.shape[0]:,}")
with col4:
    unique_types = filtered_data['Type'].nunique()
    st.metric("Unique Donation Types", f"{unique_types}")

# Donation trends over time
st.subheader("Donation Trends Over Time")
chart_type = st.selectbox("Choose chart type for donation trends", options=['Line Chart', 'Bar Chart'])
if chart_type == 'Line Chart':
    fig1 = px.line(
        filtered_data,
        x='Date',
        y='Amount',
        color='Type',
        title='Donation Trends by Type',
        labels={'Amount': 'Donation Amount', 'Date': 'Date'},
        color_discrete_sequence=px.colors.sequential.Blues
    )
else:
    fig1 = px.bar(
        filtered_data,
        x='Date',
        y='Amount',
        color='Type',
        title='Donation Trends by Type',
        labels={'Amount': 'Donation Amount', 'Date': 'Date'},
        color_discrete_sequence=px.colors.sequential.Blues
    )
st.plotly_chart(fig1, use_container_width=True)

# Rolling average trend
st.subheader("Rolling Average of Donations")
rolling_window = st.slider("Select rolling window size (in days)", min_value=1, max_value=30, value=7)
rolling_avg_data = filtered_data.set_index('Date').sort_index()['Amount'].rolling(window=rolling_window).mean().reset_index()
fig_rolling_avg = px.line(
    rolling_avg_data,
    x='Date',
    y='Amount',
    title=f'{rolling_window}-Day Rolling Average of Donations',
    labels={'Amount': 'Rolling Average Donation ($)', 'Date': 'Date'},
    color_discrete_sequence=['#1f77b4']
)
st.plotly_chart(fig_rolling_avg, use_container_width=True)

# Heatmap for donation concentration by ZIP code
st.subheader("Donation Heatmap")
heatmap_data = filtered_data.groupby('Zip')['Amount'].sum().reset_index()
fig_heatmap = px.density_heatmap(
    heatmap_data,
    x='Zip',
    y='Amount',
    title='Donation Concentration by ZIP Code',
    labels={'Amount': 'Total Donations ($)', 'Zip': 'ZIP Code'},
    color_continuous_scale='Hot'
)
fig_heatmap.update_layout(
    template='plotly_white',
    title_font_size=20,
    title_x=0.5,
    font=dict(size=14),
    xaxis=dict(tickangle=45)
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Seasonal comparison visualization with updated season names
st.subheader("Donation Amounts by Season")
seasonal_data = filtered_data.groupby('Season')['Amount'].sum().reset_index()
fig5 = px.bar(
    seasonal_data,
    x='Season',
    y='Amount',
    title='Total Donations by Season',
    labels={'Amount': 'Total Donations ($)', 'Season': 'Season'},
    color='Amount',
    color_continuous_scale='Teal'
)
fig5.update_layout(
    template='plotly_white',
    title_font_size=20,
    title_x=0.5,
    font=dict(size=14)
)
st.plotly_chart(fig5, use_container_width=True)

# Interactive map visualization
st.subheader("Interactive Map of Donations")
hover_info = st.multiselect("Select hover information", ['Type', 'Campaign', 'Amount'], default=['Type', 'Campaign', 'Amount'])
fig3 = px.scatter_mapbox(
    filtered_data,
    lat='Latitude',
    lon='Longitude',
    size='Amount',
    color='Campaign',
    hover_data=hover_info,
    title='Geographical Distribution of Donations',
    mapbox_style="open-street-map",
    zoom=10
)
fig3.update_layout(
    mapbox=dict(center=dict(lat=filtered_data['Latitude'].mean(), lon=filtered_data['Longitude'].mean())),
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig3, use_container_width=True)

# Average donation per campaign
st.subheader("Average Donation per Campaign")
fig4 = px.bar(
    filtered_data,
    x='Campaign',
    y='Amount',
    title='Average Donation per Campaign',
    labels={'Amount': 'Avg Donation ($)'},
    color='Amount',
    color_continuous_scale='Teal'
)
fig4.update_layout(
    template='plotly_white',
    title_font_size=20,
    title_x=0.5,
    font=dict(size=14)
)
st.plotly_chart(fig4, use_container_width=True)

# User notes section
st.subheader("Your Observations")
user_notes = st.text_area("Add your notes or observations about the data:")
if user_notes:
    st.write("Your Notes:")
    st.write(user_notes)

# Download filtered data
st.sidebar.sub
header("Download Options")
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_donation_data.csv',
    mime='text/csv'
)

excel_data = filtered_data.to_excel(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Filtered Data as Excel",
    data=excel_data,
    file_name='filtered_donation_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

st.sidebar.markdown("**Share this Dashboard**")
st.sidebar.text("Copy and share the URL to share filtered insights with others!")

# Feedback section for user input
feedback = st.sidebar.text_area("Please provide your feedback or suggestions:")
if feedback:
    st.sidebar.write("Thank you for your feedback!")
