import os
from google.oauth2.service_account import Credentials
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Function to authenticate and connect to Google Sheets
def authenticate_google_sheets():
    # Get the path from the environment variable
    creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')

    if not creds_path:
        raise Exception("The environment variable for credentials path is not set.")

    # Use the credentials from the file
    creds = Credentials.from_service_account_file(creds_path)
    client = gspread.authorize(creds)
    return client

# Function to open and return the worksheet
def get_spreadsheet(sheet_name, worksheet_name):
    client = authenticate_google_sheets()
    spreadsheet = client.open(sheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet

# Function to update a record in Google Sheets
def update_google_sheet(name, bowls_issued, amount_paid):
    sheet_name = 'Your Google Sheet Name'
    worksheet_name = 'Your Worksheet Name'
    worksheet = get_spreadsheet(sheet_name, worksheet_name)

    # Get the next available row to insert the new record
    next_row = len(worksheet.get_all_values()) + 1

    # Append the data to the Google Sheet (replace column indices with actual column numbers)
    worksheet.update_cell(next_row, 1, name)
    worksheet.update_cell(next_row, 2, bowls_issued)
    worksheet.update_cell(next_row, 3, amount_paid)

# Streamlit form and logic
people = ['Micheal', 'TKW', 'CLE', 'TAP']
cost_per_bowl = 0.19

# Sidebar for user selection
st.sidebar.title("Record Bowls Issued")

# User selects the name from a dropdown
name = st.sidebar.selectbox("Select Name of Person:", people)

# User selects the number of bowls from a dropdown
bowls_issued = st.sidebar.selectbox("Select Number of Bowls:", list(range(10, 151, 10)))

# Calculate the total amount after 70% subsidy
subsidy = 0.70
total_cost = cost_per_bowl * bowls_issued
amount_paid = total_cost * (1 - subsidy)

# Display the calculated amount
st.write(f"Total Amount Paid After 70% Subsidy: ${amount_paid:.2f}")

# Save the data to Google Sheets
if st.sidebar.button("Submit"):
    update_google_sheet(name, bowls_issued, amount_paid)
    st.success("Record saved to Google Sheets!")

