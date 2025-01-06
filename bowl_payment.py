import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


# Streamlit secrets management: Store the credentials.json content in the secrets.toml file
# Create a secrets.toml file in your Streamlit app with the content below:
# [google]
# credentials = "your_json_content_here"
google_credentials = {
    "client_id": st.secrets["google"]["client_id"],
    "project_id": st.secrets["google"]["project_id"],
    "auth_uri": st.secrets["google"]["auth_uri"],
    "token_uri": st.secrets["google"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
    "client_secret": st.secrets["google"]["client_secret"]
}

def authenticate_gspread():
    # Fetch credentials from secrets
    creds_json = st.secrets["google"]["credentials"]
    creds = Credentials.from_service_account_info(google_credentials)

    # Authorize with gspread
    client = gspread.authorize(creds)
    return client


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
