import streamlit as st
import pandas as pd

# Load the startup funding data
df = pd.read_csv("Startup_Cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Funding Analysis')

# Preprocess the date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


# Function to load investor details
def load_investor_details(investor):
    st.title(investor)
    st.subheader('Investor Analysis')

    investor_data = df[df['investors'].str.contains(investor, na=False)]

    # Display recent investments by the investor
    st.subheader('Recent Investments')
    st.dataframe(investor_data[['startup', 'vertical', 'city', 'round', 'amount']].head())

    # Display maximum investment
    max_investment = investor_data.groupby('startup')['amount'].sum().nlargest(1)
    st.subheader('Maximum Investment')
    st.dataframe(max_investment)


# Function to load startup details
def load_startup_details(startup_name):
    st.title(startup_name)
    st.subheader('Startup Analysis')

    startup_data = df[df['startup'] == startup_name].iloc[0]

    # Display basic startup information
    st.subheader('Basic Information')
    st.write(f"Name: {startup_data['startup']}")
    st.write(f"investors: {startup_data['investors']}")
    st.write(f"Industry: {startup_data['vertical']}")
    st.write(f"Subindustry: {startup_data['subvertical']}")
    st.write(f"Location: {startup_data['city']}")

    # Display funding rounds
    st.subheader('Funding Rounds')
    st.dataframe(df[df['startup'] == startup_name][['round', 'investors', 'date']])


# Sidebar title and option selection
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.radio('Select Analysis Type', ['Overall Analysis', 'Startup Analysis', 'Investor Analysis'])

# Perform analysis based on selected option
if option == 'Investor Analysis':
    selected_investor = st.sidebar.selectbox('Select Investor', df['investors'].unique())
    load_investor_details(selected_investor)

elif option == 'Startup Analysis':
    selected_startup = st.sidebar.selectbox('Select Startup', df['startup'].unique())
    load_startup_details(selected_startup)

else:
    st.title("Overall Analysis")
    st.header("MoM graph")
    selected_option = st.selectbox("Select Type", ["Total", "Count"])
    if selected_option == "Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x_axis"] = temp_df["month"].astype("str") + '-' + temp_df["year"].astype("str")

    st.line_chart(temp_df.set_index("x_axis"))

    st.subheader("Top Sectors (Count)")
    top_sectors_count = df['vertical'].value_counts().nlargest(5)
    st.write(top_sectors_count)

    st.subheader("Top Sectors (Sum)")
    top_sectors_sum = df.groupby('vertical')['amount'].sum().nlargest(5)
    st.write(top_sectors_sum)

    st.subheader("Type of Funding")
    funding_types = df['round'].value_counts()
    st.write(funding_types)

    st.subheader("Top Investors")
    top_investors = df.groupby('investors')['amount'].sum().nlargest(5)
    st.write(top_investors)
