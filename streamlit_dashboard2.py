import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data_path = '/Users/leontang/Downloads/skunkworks_data_v6.csv'  # Ensure this file path is correct and accessible
data = pd.read_csv(data_path)

# Streamlit app layout
st.set_page_config(page_title="Interactive Donation Dashboard", layout="wide")
st.title("Interactive Donation Data Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    [pd.to_datetime(data['Date']).min(), pd.to_datetime(data['Date']).max()]
)
selected_type = st.sidebar.multiselect("Select Type", data['Type'].unique(), default=data['Type'].unique())
selected_campaign = st.sidebar.multiselect("Select Campaign", data['Campaign'].unique(), default=data['Campaign'].unique())
selected_zip = st.sidebar.multiselect("Select ZIP Code", data['Zip'].dropna().unique(), default=data['Zip'].dropna().unique())
min_donation = st.sidebar.slider("Minimum Donation Amount", min_value=float(data['Amount'].min()), max_value=float(data['Amount'].max()), value=float(data['Amount'].min()))
max_donation = st.sidebar.slider("Maximum Donation Amount", min_value=float(data['Amount'].min()), max_value=float(data['Amount'].max()), value=float(data['Amount'].max()))

# Apply filters
filtered_data = data[
    (pd.to_datetime(data['Date']) >= pd.to_datetime(selected_date_range[0])) &
    (pd.to_datetime(data['Date']) <= pd.to_datetime(selected_date_range[1])) &
    (data['Type'].isin(selected_type)) &
    (data['Campaign'].isin(selected_campaign)) &
    (data['Zip'].isin(selected_zip)) &
    (data['Amount'] >= min_donation) &
    (data['Amount'] <= max_donation)
]

# Display filtered data overview
st.subheader("Filtered Data Overview")
st.dataframe(filtered_data)

# Sidebar additional insights
st.sidebar.subheader("Additional Insights")
st.sidebar.write("**Total Donations Amount:** ${:,.2f}".format(filtered_data['Amount'].sum()))
st.sidebar.write("**Average Donation Amount:** ${:,.2f}".format(filtered_data['Amount'].mean()))
st.sidebar.write("**Total Number of Transactions:** {:,}".format(filtered_data.shape[0]))

# Color theme selection for charts
color_theme = st.sidebar.selectbox(
    "Select Color Theme",
    options=['Blues', 'Viridis', 'Magma', 'Cividis', 'Plasma']
)

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
        color_discrete_sequence=px.colors.sequential.__dict__[color_theme]
    )
else:
    fig1 = px.bar(
        filtered_data,
        x='Date',
        y='Amount',
        color='Type',
        title='Donation Trends by Type',
        labels={'Amount': 'Donation Amount', 'Date': 'Date'},
        color_discrete_sequence=px.colors.sequential.__dict__[color_theme]
    )
st.plotly_chart(fig1, use_container_width=True)

# Top ZIP code filter and visualization
st.sidebar.subheader("Top ZIP Code Filter")
top_n_zip_codes = st.sidebar.slider("Select number of top ZIP codes to display", min_value=5, max_value=50, value=10, step=5)

# Calculate top ZIP codes by total donations
top_zip_data = (
    filtered_data.groupby('Zip')['Total Donations per Zip']
    .sum()
    .sort_values(ascending=False)
    .head(top_n_zip_codes)
    .reset_index()
)

st.subheader(f"Top {top_n_zip_codes} ZIP Codes by Total Donations")
fig2 = px.bar(
    top_zip_data,
    y='Zip',
    x='Total Donations per Zip',
    orientation='h',
    title=f'Top {top_n_zip_codes} ZIP Codes by Total Donations',
    labels={'Zip': 'ZIP Code', 'Total Donations per Zip': 'Total Donations'},
    color='Total Donations per Zip',
    color_continuous_scale=color_theme
)
fig2.update_layout(
    xaxis_title='Total Donations ($)',
    yaxis_title='ZIP Code',
    template='plotly_white',
    title_font_size=20,
    title_x=0.5,
    font=dict(size=14),
    showlegend=False
)
fig2.update_traces(
    texttemplate='%{x:,.2f}',
    textposition='auto'
)
st.plotly_chart(fig2, use_container_width=True)

# Seasonal comparison visualization
st.subheader("Donation Amounts by Season")
seasonal_data = filtered_data.groupby('Season')['Amount'].sum().reset_index()
fig5 = px.bar(
    seasonal_data,
    x='Season',
    y='Amount',
    title='Total Donations by Season',
    labels={'Amount': 'Total Donations ($)', 'Season': 'Season'},
    color='Amount',
    color_continuous_scale=color_theme
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
    y='Average Donation per Campaign',
    title='Average Donation per Campaign',
    labels={'Average Donation per Campaign': 'Avg Donation ($)'},
    color='Average Donation per Campaign',
    color_continuous_scale=color_theme
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
st.sidebar.subheader("Download Options")
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_donation_data.csv',
    mime='text/csv'
)

st.sidebar.markdown("**Share this Dashboard**")
st.sidebar.text("Copy and share the URL to share filtered insights with others!")
