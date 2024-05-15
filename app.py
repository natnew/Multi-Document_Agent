import streamlit as st
import pandas as pd
import pdfplumber
import io
import matplotlib.pyplot as plt
import plotly.express as px

# Title of the app
st.title('Streamlit App for CSV and PDF Files')

# Description
st.write("""
This is a Streamlit app that accepts both CSV and PDF files, displays their content, and creates basic visualizations for CSV data.
""")

# File uploader for CSV or PDF files
uploaded_file = st.file_uploader("Choose a CSV or PDF file", type=["csv", "pdf"])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    
    if uploaded_file.type == "application/pdf":
        # Handling PDF files
        st.write("PDF File Details:", file_details)
        
        # Extracting text from PDF
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() + "\n"
        
        # Display extracted text
        st.write("Extracted Text:")
        st.text(all_text)
    
    elif uploaded_file.type == "text/csv":
        # Handling CSV files
        st.write("CSV File Details:", file_details)
        
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)
        
        # Display the dataframe
        st.write("Dataframe:")
        st.dataframe(data)
        
        # Display basic statistics
        st.write("Basic Statistics:")
        st.write(data.describe())
        
        # Display a line chart
        st.write("Line Chart:")
        st.line_chart(data)
        
        # Display a bar chart using Plotly
        st.write("Bar Chart:")
        fig = px.bar(data, x=data.columns[0], y=data.columns[1])
        st.plotly_chart(fig)
        
        # Display a matplotlib plot
        st.write("Histogram:")
        fig, ax = plt.subplots()
        ax.hist(data[data.columns[1]], bins=20)
        st.pyplot(fig)
else:
    st.write("Please upload a CSV or PDF file to get started.")

# Footer
st.write("""
### Thank you for using this app!
""")
