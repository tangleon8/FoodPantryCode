import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import io

data_path = '/Users/leontang/Downloads/skunkworks_data_v6.csv'
data = pd.read_csv(data_path)

data['Date'] = pd.to_datetime(data['Date'])

# Clean ZIP codes by removing commas and leading/trailing spaces
data['Zip'] = data['Zip'].astype(str).str.replace(',', '').str.strip()

# Map numeric or coded seasons to actual season names
season_mapping = {
    1: 'Winter',
    2: 'Spring',
    3: 'Summer',
    4: 'Fall'
}
data['Season'] = data['Season'].map(season_mapping)

# Filter data to only include Wisconsin ZIP codes (ZIPs starting with '53')
wisconsin_data = data[data['Zip'].str.startswith('53')]

# Set up the Streamlit app's page configuration
st.set_page_config(page_title="Interactive Donation Dashboard", layout="wide")
st.title("Interactive Donation Data Dashboard")

# Sidebar: Filter options
st.sidebar.header("Filter Options")

# Default filter values
default_date_range = [data['Date'].min(), data['Date'].max()]
all_types = list(data['Type'].unique())
all_campaigns = list(data['Campaign'].unique())
all_zips = list(wisconsin_data['Zip'].unique())
default_min_donation = float(data['Amount'].min())
default_max_donation = float(data['Amount'].max())

# Sidebar: Reset filters button
if st.sidebar.button("Reset Filters"):
    selected_date_range = default_date_range
    selected_type = all_types
    selected_campaign = all_campaigns
    selected_zip = all_zips
    min_donation = default_min_donation
    max_donation = default_max_donation
else:
    # Sidebar: Date range filter
    selected_date_range = st.sidebar.date_input(
        "Select Date Range",
        default_date_range
    )

    # Sidebar: Dual-list multiselect for donation Type
    selected_type = st.sidebar.multiselect("Selected Types", all_types, default=all_types)

    # Sidebar: Dual-list multiselect for Campaign
    selected_campaign = st.sidebar.multiselect("Selected Campaigns", all_campaigns, default=all_campaigns)

    # Sidebar: Dual-list multiselect for ZIP code (Wisconsin only)
    selected_zip = st.sidebar.multiselect("Selected ZIP Codes", all_zips, default=all_zips)

    # Sidebar: Slider for minimum and maximum donation amounts
    min_donation = st.sidebar.slider(
        "Minimum Donation Amount",
        min_value=default_min_donation,
        max_value=default_max_donation,
        value=default_min_donation
    )
    max_donation = st.sidebar.slider(
        "Maximum Donation Amount",
        min_value=default_min_donation,
        max_value=default_max_donation,
        value=default_max_donation
    )

# Apply the selected filters to the dataset
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

# Display dynamic summary metrics
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

# Visualize donation trends over time
st.subheader("Donation Trends Over Time")
chart_type = st.selectbox("Choose chart type for donation trends", options=['Line Chart', 'Bar Chart'])
if chart_type == 'Line Chart':
    fig1 = px.line(
        filtered_data,
        x='Date',
        y='Amount',
        color='Type',
        title='Donation Trends by Type',
        labels={'Amount': 'Donation Amount', 'Date': 'Date'}
    )
else:
    fig1 = px.bar(
        filtered_data,
        x='Date',
        y='Amount',
        color='Type',
        title='Donation Trends by Type',
        labels={'Amount': 'Donation Amount', 'Date': 'Date'}
    )
st.plotly_chart(fig1, use_container_width=True)

# Calculate and visualize rolling average trends
st.subheader("Rolling Average of Donations")
rolling_window = st.slider("Select rolling window size (in days)", min_value=1, max_value=30, value=7)
rolling_avg_data = filtered_data.set_index('Date').sort_index()['Amount'].rolling(window=rolling_window).mean().reset_index()
fig_rolling_avg = px.line(
    rolling_avg_data,
    x='Date',
    y='Amount',
    title=f'{rolling_window}-Day Rolling Average of Donations',
    labels={'Amount': 'Rolling Average Donation ($)', 'Date': 'Date'}
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
fig_heatmap.update_layout(template='plotly_white')
st.plotly_chart(fig_heatmap, use_container_width=True)

# Visualize total donations by season
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
st.plotly_chart(fig5, use_container_width=True)

# Interactive map visualization for geographical donation data
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
    mapbox_style="open-street-map"
)
fig3.update_layout(
    mapbox=dict(center=dict(lat=filtered_data['Latitude'].mean(), lon=filtered_data['Longitude'].mean())),
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig3, use_container_width=True)

# Average donation per campaign visualization
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
st.plotly_chart(fig4, use_container_width=True)

# User notes section to document insights or observations
st.subheader("Your Observations")
user_notes = st.text_area("Add your notes or observations about the data:")
if user_notes:
    st.write("Your Notes:")
    st.write(user_notes)

csv = filtered_data.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_donation_data.csv',
    mime='text/csv'
)

excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    filtered_data.to_excel(writer, index=False)
# Reset the buffer's position to the beginning
excel_buffer.seek(0)

st.sidebar.download_button(
    label="Download Filtered Data as Excel",
    data=excel_buffer,
    file_name='filtered_donation_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# "run streamlit dashboard.py" in your terminal to run this file 
