import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import json

# Authenticate and fetch credentials from Streamlit secrets
def authenticate_gspread():
    try:
        # Fetch the credentials securely from Streamlit secrets
        google_creds = st.secrets["google"]

        # Define the required scopes for Google Sheets and Google Drive
        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",  # Full access to Google Sheets
            "https://www.googleapis.com/auth/drive"  # Full access to Google Drive
        ]

        # Create credentials from the service account information stored in Streamlit secrets
        creds = Credentials.from_service_account_info(google_creds, scopes=SCOPES)

        # Check if the credentials are valid, and refresh if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())  # This should refresh the token

        # Authorize with gspread
        client = gspread.authorize(creds)
        return client

    except Exception as e:
        # Catch any other exceptions and display them
        st.error(f"An error occurred: {str(e)}")
        raise e

# Connect to the Google Sheets
def update_sheet(client, name, bowls, amount_before_subsidy, amount_after_subsidy):
    sheet = client.open('BowlsPaymentRecord')  # Open your sheet by name
    worksheet = sheet.sheet1  # Access the first worksheet
    worksheet.append_row([name, bowls, amount_before_subsidy, amount_after_subsidy])

# Calculate the amount to pay after 70% subsidy
def calculate_amount(bowls):
    cost_per_bowl = 0.19
    total_amount = bowls * cost_per_bowl
    amount_after_subsidy = total_amount * 0.3  # 70% subsidy
    return total_amount, amount_after_subsidy

# Streamlit app
def main():
    st.title("Bowls Payment Recorder")

    # Define a list of people (can be expanded as needed)
    people = ["Micheal", "TKW", "CLE", "TAP"]

    # Combo box for selecting person
    name = st.selectbox("Select Person", people)

    # Combo box for selecting number of bowls (with intervals of 10 between 10 and 150)
    bowls = st.selectbox("Select Number of Bowls", [i for i in range(10, 151, 10)])

    # Calculate the amount to pay
    amount_before, amount_after = calculate_amount(bowls)

    st.write(f"Amount before subsidy: ${amount_before:.2f}")
    st.write(f"Amount after 70% subsidy: ${amount_after:.2f}")

    # Submit button to update the record
    if st.button("Submit Record"):
        client = authenticate_gspread()
        update_sheet(client, name, bowls, amount_before, amount_after)
        st.success("Record updated successfully!")

if __name__ == "__main__":
    main()