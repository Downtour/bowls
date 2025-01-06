import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st


# Authentication for Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('hgfo8sq803asl9nusq0q0dnp8seigdq1.apps.googleusercontent.com.json', scope)
    client = gspread.authorize(creds)
    return client


# Create or access the Google Sheet
def get_or_create_spreadsheet(client):
    try:
        # Open the existing spreadsheet by name
        sheet = client.open('Bowl Payment Records').sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        # If the sheet does not exist, create one
        sheet = client.create('Bowl Payment Records').sheet1
        # Add headers if creating the sheet
        sheet.append_row(['Name', 'Number of Bowls', 'Original Price', 'Subsidized Price'])

    return sheet

def calculate_payment(number_of_bowls):
    bowl_cost = 0.19
    total_cost = bowl_cost * number_of_bowls
    subsidized_cost = total_cost * 0.3  # 70% subsidy, so you pay 30%
    return total_cost, subsidized_cost


def main():
    st.title('Bowl Payment Calculator')

    # User inputs
    name = st.text_input('Enter Name:')
    number_of_bowls = st.number_input('Enter Number of Bowls:', min_value=1, step=1)

    # Button to submit
    if st.button('Calculate Payment'):
        if name and number_of_bowls:
            # Calculate the payment
            total_cost, subsidized_cost = calculate_payment(number_of_bowls)

            st.write(f'Total Cost: ${total_cost:.2f}')
            st.write(f'Subsidized Cost (30% of Total): ${subsidized_cost:.2f}')

            # Authenticate and get the spreadsheet
            client = authenticate_google_sheets()
            sheet = get_or_create_spreadsheet(client)

            # Append the record to the Google Sheet
            sheet.append_row([name, number_of_bowls, f"${total_cost:.2f}", f"${subsidized_cost:.2f}"])

            st.success('Record added to Google Sheets!')
        else:
            st.error('Please enter valid details.')


if __name__ == '__main__':
    main()

