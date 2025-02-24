import streamlit as st
import pandas as pd
import re
from googlesearch import search
from time import sleep

def find_company_emails(company_name):
    """Search Google for company emails and extract using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    query = f'"{company_name}" "company email"'
    
    try:
        # Search Google with 3 results and 2 sec delay between requests
        search_results = search(query, num_results=3, sleep_interval=2)
        
        # Check first 3 results for email addresses
        for url in search_results:
            response = requests.get(url, timeout=10)
            emails = re.findall(email_pattern, response.text)
            if emails:
                return ', '.join(list(set(emails)))
    
    except Exception as e:
        return f"Error: {str(e)}"
    
    return "No email found"

st.title("Company Email Finder 🕵️")
st.write("Upload CSV with company names in first column to find associated emails")

uploaded_file = st.file_uploader("Choose CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    company_column = df.columns[0]
    
    if st.button("Find Emails"):
        with st.status("Searching for emails...", expanded=True) as status:
            # Add email column if not exists
            if 'Email' not in df.columns:
                df['Email'] = ''
            
            # Process each company
            for index, row in df.iterrows():
                company = row[company_column]
                if pd.notna(company):
                    st.write(f"Searching for: {company}")
                    df.at[index, 'Email'] = find_company_emails(str(company))
                    sleep(1)  # Add delay between searches
            
            status.update(label="Search complete!", state="complete")
        
        st.dataframe(df)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name='company_emails.csv',
            mime='text/csv'
        )
