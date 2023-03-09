import streamlit as st
import pandas as pd
import datetime

from oscndocketscraper import OSCNDocketScraper
from oscncasescraper import OSCNCaseScraper

# Calculate total fees paid
def calculate_total_fees(df):
    # calculate total fees paid
    total_fees = df['amount'].sum()
    return total_fees

# Calculate number of consecutive months paid
def calculate_consecutive_months(df):
    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # generate a list of consecutive months
    month_list = []
    for i in range(len(df)-1):
        current_month = df['date'][i].month
        next_month = df['date'][i+1].month
        if (next_month - current_month) == 1:
            month_list.append(current_month)
        else:
            month_list.append(current_month)
            month_list.append('break')

    # loop through the month list to find the longest consecutive sequence
    max_consecutive = 0
    consecutive_count = 0
    for month in month_list:
        if month != 'break':
            consecutive_count += 1
            if consecutive_count > max_consecutive:
                max_consecutive = consecutive_count
        else:
            consecutive_count = 0

    return max_consecutive

# Cache the data for faster retrieval
@st.cache_data
def scrape_multiple_cases(url_list, first_name, last_name, middle_name):
    # Create a list to store the fee tables
    fee_table_list = []

    # Loop through the URLs and create an instance of the OSCNCaseScraper class for each URL
    for url in url_list:
        scraper = OSCNCaseScraper(url, first_name, last_name, middle_name)
        try:
            fee_table_list.append(scraper.fee_table)
            st.write(f"{scraper.case_number}: {len(scraper.fee_table)} results")
        except:
            st.write(f"{scraper.case_number}: 0 results")

    # Concatenate the fee tables into one overall fee table
    overall_fee_table = pd.concat(fee_table_list)
    # Convert the date column to datetime and extract just the date portion
    overall_fee_table['date'] = pd.to_datetime(overall_fee_table['date']).dt.date
    # Sort the fee table by date
    overall_fee_table.sort_values(by='date', inplace=True)

    return overall_fee_table.reset_index(drop=True)

# Define a function to format the date
def format_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date

# Cache the data for faster retrieval
@st.cache_data
def get_data(first_name, last_name, middle_name='', db='all') -> pd.DataFrame:
    docket_scraper = OSCNDocketScraper(db='all', first_name='Leroy', last_name='Jordan', middle_name='Albert')
    results = docket_scraper.scrape_results()
    # Convert the date_filed column to datetime and extract just the date portion
    results['date_filed'] = pd.to_datetime(results['date_filed']).dt.date
    # Insert a 'keep' column with all values initially set to True
    results.insert(0, 'keep', False)
    return results.reset_index(drop=True)

# Create a Streamlit app
st.title("Fines & Fees Waiver Automation")

st.subheader("Enter Name")
st.markdown("Please enter first name, middle name, and last name separated by commas (e.g. John,Michael,Smith), then press enter.")

# Create a text input field for the user to enter their name
name_input = st.text_input("")

# Parse the name input into first name, middle name, and last name
if name_input:
    name_parts = name_input.split(",")
    first_name = name_parts[0].strip()
    middle_name = name_parts[1].strip()
    last_name = name_parts[2].strip()

    df = get_data(first_name, last_name, middle_name)
    # Use the experimental data editor to allow the user to select which rows to keep
    edited_df = st.experimental_data_editor(
        df.drop(columns=['url']),
        use_container_width=True,
        num_rows="dynamic",
    )

    if st.button("Done selecting? Click here to pull data."):
        # Get the indices of the rows that the user wants to keep
        keep_rows = edited_df.loc[edited_df['keep'] == True].index.tolist()
        # Get the corresponding URLs from the original dataframe
        url_list = df.loc[keep_rows, 'url'].tolist()

        st.write(url_list)
        fee_tables = scrape_multiple_cases(url_list, first_name, last_name, middle_name)
        st.write(fee_tables)

        total_fees = calculate_total_fees(fee_tables)
        total_fees = round(total_fees, 2)
        max_consecutive = calculate_consecutive_months(fee_tables)

        st.write("Total Fees Paid: ", total_fees)
        st.write("Consecutive Months Paid: ", max_consecutive)






