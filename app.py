import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Title of the app
st.title('Simple Streamlit App')

# Description
st.write("""
This is a simple Streamlit app that demonstrates basic functionality including data display and visualization.
""")

# File uploader for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
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
    st.write("Please upload a CSV file to get started.")

# Footer
st.write("""
### Thank you for using this app!
""")
