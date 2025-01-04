import streamlit as st
import csv

# List of names to choose from (example data)
people = ['Micheal', 'KW', 'CLE', 'TAP']

# Cost per bowl
cost_per_bowl = 0.19

# Sidebar for user selection
st.sidebar.title("Record Bowls Issued")

# User selects the name from a dropdown
name = st.sidebar.selectbox("Select Name of Person receiving the bowls:", people)

# User selects the number of bowls from a dropdown
bowls_issued = st.sidebar.selectbox("Select Number of Bowls:", list(range(10, 151, 10)))

# Calculate the total amount after 70% subsidy
subsidy = 0.70
total_cost = cost_per_bowl * bowls_issued
amount_paid = total_cost * (1 - subsidy)

# Display the calculated amount
st.write(f"Total Amount Paid After 70% Subsidy: ${amount_paid:.2f}")

# Save the data to CSV
if st.sidebar.button("Submit"):
    with open('records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, bowls_issued, amount_paid])
    st.success("Record saved!")