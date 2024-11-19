import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Load the data
data_path = '/Users/leontang/Downloads/skunkworks_data_v6.csv'  # Ensure this file path is correct and accessible
data = pd.read_csv(data_path)

# Convert the 'Date' column to datetime if not already
data['Date'] = pd.to_datetime(data['Date'])

# Streamlit app layout
st.set_page_config(page_title="Interactive Donation Dashboard", layout="wide")
st.title("Interactive Donation Data Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a page:", ["Overview", "Trends & Analysis", "Comparative Analysis", "Data Table"])

# Convert min and max dates to datetime.date for the slider
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
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

# Overview page
if page == "Overview":
    st.header("Overview of Filtered Data")
    st.dataframe(filtered_data)

    # Summary metrics
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

    # Additional sidebar insights
    st.sidebar.subheader("Detailed Insights")
    st.sidebar.write("**Top Donation Type Percentage:**")
    if unique_types > 0:
        type_counts = filtered_data['Type'].value_counts(normalize=True).head(1) * 100
        st.sidebar.write(f"{type_counts.index[0]}: {type_counts.iloc[0]:.2f}%")

# Trends & Analysis page
elif page == "Trends & Analysis":
    st.header("Trends & Analysis")

    # Color theme selection for charts
    color_theme = st.sidebar.selectbox(
        "Select Color Theme",
        options=['Blues', 'Viridis', 'Magma', 'Cividis', 'Plasma']
    )

    # Interactive date range slider for filtering
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
    st.plotly_chart(fig5, use_container_width=True)

    # Highlight significant data points
    st.subheader("Highlight Significant Points")
    highlight = st.button("Highlight Outliers")
    if highlight:
        st.write("Outliers are shown as red points.")
        fig1.add_trace(go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data['Amount'],
            mode='markers',
            marker=dict(color='red', size=10),
            name='Outliers'
        ))
        st.plotly_chart(fig1, use_container_width=True)

# Comparative Analysis page
elif page == "Comparative Analysis":
    st.header("Comparative Analysis Tool")
    comparison_metric = st.radio("Choose a metric to compare:", ["ZIP Code", "Campaign"])

    if comparison_metric == "ZIP Code":
        zip1 = st.selectbox("Select first ZIP Code", filtered_data['Zip'].unique())
        zip2 = st.selectbox("Select second ZIP Code", filtered_data['Zip'].unique())

        data_zip1 = filtered_data[filtered_data['Zip'] == zip1]
        data_zip2 = filtered_data[filtered_data['Zip'] == zip2]

        st.write(f"**Comparing donations between ZIP Code {zip1} and {zip2}**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"Total Donations in {zip1}", f"${data_zip1['Amount'].sum():,.2f}")
            st.metric(f"Average Donation in {zip1}", f"${data_zip1['Amount'].mean():,.2f}")
        with col2:
            st.metric(f"Total Donations in {zip2}", f"${data_zip2['Amount'].sum():,.2f}")
            st.metric(f"Average Donation in {zip2}", f"${data_zip2['Amount'].mean():,.2f}")

    elif comparison_metric == "Campaign":
        campaign1 = st.selectbox("Select first Campaign", filtered_data['Campaign'].unique())
        campaign2 = st.selectbox("Select second Campaign", filtered_data['Campaign'].unique())

        data_campaign1 = filtered_data[filtered_data['Campaign'] == campaign1]
        data_campaign2 = filtered_data[filtered_data['Campaign'] == campaign2]

        st.write(f"**Comparing donations between Campaign {campaign1} and {campaign2}**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"Total Donations in {campaign1}", f"${data_campaign1['Amount'].sum():,.2f}")
            st.metric(f"Average Donation in {campaign1}", f"${data_campaign1['Amount'].mean():,.2f}")
        with col2:
            st.metric(f"Total Donations in {campaign2}", f"${data_campaign2['Amount'].sum():,.2f}")
            st.metric(f"Average Donation in {campaign2}", f"${data_campaign2['Amount'].mean():,.2f}")

# Data Table page
elif page == "Data Table":
    st.header("Searchable Data Table")
    st.dataframe(filtered_data)

    # Add search and sort features
    search_query = st.text_input("Search for specific text in the data:")
    if search_query:
        filtered_search_data = filtered_data[filtered_data.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        st.dataframe(filtered_search_data)
    else:
        st.dataframe(filtered_data)

    st.sidebar.subheader("Download Options")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_donation_data.csv',
        mime='text/csv'
    )
