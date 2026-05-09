"""
Chat with Customer Data - Streamlit Application
"""

import streamlit as st
import pandas as pd
from data_loader import load_excel_data
from query_engine import create_query_engine

# API Key - Add your Gemini API key here
API_KEY = "AIzaSyBNtJXzXMwVdBpLMyDDvIa53c2keAca4Ew"

# Page title
st.title("Chat with Customer Data")
st.write("Upload your Excel file and ask questions in plain English")

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'], label_visibility="collapsed")
st.caption("Supported formats: .xlsx, .xls")

if uploaded_file is not None:
    # Load data
    df = load_excel_data(uploaded_file)


    # Question input
    st.subheader("Ask a Question")
    question = st.text_input("Enter your question:")

    # Example questions
    st.write("Examples: How many records? What is the average of [column]? List unique values in [column]")

    # Process question
    if st.button("Get Answer"):
        if not question:
            st.warning("Please enter a question")
        else:
            with st.spinner("Processing..."):
                engine = create_query_engine(API_KEY, df)
                result = engine.query(question)

            if result['success']:
                # Show summary first (the human-readable answer)
                if result['summary']:
                    st.write(result['summary'])
                # Show data only if it's actual useful data
                answer = result['answer']
                if answer and answer != 'None' and 'NaN' not in answer and 'No records found' not in answer and len(answer) < 2000:
                    st.write(answer)
            else:
                st.error(result['answer'])
else:
    st.info("Please upload an Excel file to get started")
