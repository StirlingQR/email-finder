import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Function to extract company email
def fetch_company_email(company_name):
    search_query = f"{company_name} contact email"
    google_search_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(google_search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract email-like text from search results
        for link in soup.find_all("a"):
            href = link.get("href", "")
            if "mailto:" in href:
                return href.split(":")[1]
    except Exception as e:
        return None
    return None

# Streamlit app layout
st.title("Company Email Finder")
st.write("Upload a CSV file with a list of company names to find their contact emails.")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)
    if "Company" not in df.columns:
        st.error("CSV must contain a 'Company' column.")
    else:
        st.write("Processing your data...")
        df["Email"] = df["Company"].apply(fetch_company_email)
        
        # Display results
        st.write("Results:")
        st.dataframe(df)
        
        # Download results as Excel
        @st.cache_data
        def convert_df_to_excel(dataframe):
            output = pd.ExcelWriter("output.xlsx", engine="openpyxl")
            dataframe.to_excel(output, index=False, sheet_name="Results")
            output.close()
            return output
            
        excel_file = convert_df_to_excel(df)
        
        st.download_button(
            label="Download Results as Excel",
            data=excel_file,
            file_name="company_emails.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
