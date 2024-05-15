import streamlit as st
import pandas as pd
import pdfplumber
import openai
import nest_asyncio
from pathlib import Path
from helper import get_openai_api_key
from utils import get_doc_tools
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex

# Apply nest_asyncio
nest_asyncio.apply()

# Setup OpenAI API key
OPENAI_API_KEY = get_openai_api_key()
openai.api_key = OPENAI_API_KEY

st.title('Streamlit App for Conversational PDF Interaction')

# File uploader for CSV or PDF files
uploaded_file = st.file_uploader("Choose a CSV or PDF file", type=["csv", "pdf"])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    
    if uploaded_file.type == "application/pdf":
        st.write("PDF File Details:", file_details)
        
        # Save the uploaded PDF
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        paper = uploaded_file.name
        vector_tool, summary_tool = get_doc_tools(paper, Path(paper).stem)
        
        llm = OpenAI(model="gpt-3.5-turbo")
        
        agent_worker = FunctionCallingAgentWorker.from_tools(
            [vector_tool, summary_tool], 
            llm=llm, 
            verbose=True
        )
        agent = AgentRunner(agent_worker)
        
        user_query = st.text_input("Ask something about the paper:")
        if user_query:
            response = agent.query(user_query)
            st.write(str(response))
    
    elif uploaded_file.type == "text/csv":
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
        import plotly.express as px
        fig = px.bar(data, x=data.columns[0], y=data.columns[1])
        st.plotly_chart(fig)
        
        # Display a matplotlib plot
        st.write("Histogram:")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.hist(data[data.columns[1]], bins=20)
        st.pyplot(fig)
else:
    st.write("Please upload a CSV or PDF file to get started.")

st.write("### Thank you for using this app!")
