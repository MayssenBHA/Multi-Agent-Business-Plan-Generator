import os
from dotenv import load_dotenv
import streamlit as st
from multiagent import app

load_dotenv()

st.title("🔍 Business Plan Generator")

company_query = st.text_input("Enter a company or industry name")

if st.button("Generate Report"):
    if company_query.strip():
        with st.spinner("Generating report..."):
            output = app.invoke({"user_input": company_query})

        st.header(f"Market Research for: {company_query}")
        st.subheader("Extracted Information:")
        st.write(output.get("company_info", "No data"))

        st.subheader("Generated Business Plan:")
        st.write(output.get("business_plan", "No data"))
    else:
        st.error("Please enter a valid input.")
