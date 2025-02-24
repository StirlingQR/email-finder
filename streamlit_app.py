import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import io

# Function to fetch company email using DuckDuckGo search
def fetch_company_email(company_name):
    search_query = f"{company_name} contact email"
    duckduckgo_url = f"https://html.duckduckgo.com/html/?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(duckduckgo_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract potential emails using regex
        potential_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text)

        # Filter emails based on specific prefixes
        valid_prefixes = ["info@", "hr@", "talent@", "recruitment@", "ta@", "recruit@", "humanresources@"]
        filtered_emails = [email for email in potential_emails if any(email.lower().startswith(prefix) for prefix in valid_prefixes)]

        if filtered_emails:
            return filtered_emails[0]  # Return the first matching email
    except Exception as e:
        return None

    return None  # Return None if no valid email is found

# Function to convert DataFrame to Excel file
def convert_df_to_excel(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Results")
    processed_data = output.getvalue()
    return processed_data

# Streamlit app layout
st.title("Company Email Finder")
st.write("Upload a CSV file with a list of company names to find their contact emails.")

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Company" not in df.columns:
        st.error("CSV must contain a 'Company' column.")
    else:
        st.write("Processing your data...")
        
        # Fetch emails for each company name in the CSV file
        df["Email"] = df["Company"].apply(fetch_company_email)
        
        # Display results in a table format within Streamlit UI
        st.write("Results:")
        st.dataframe(df)
        
        # Create and download Excel file with results
        excel_file = convert_df_to_excel(df)
        
        st.download_button(
            label="Download Results as Excel",
            data=excel_file,
            file_name="company_emails.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
