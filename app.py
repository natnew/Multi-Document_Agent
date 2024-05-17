import streamlit as st
import pandas as pd
import pdfplumber
import openai
import nest_asyncio
from pathlib import Path
from modules.helper import get_openai_api_key
from modules.utils import get_doc_tools
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner

# Apply nest_asyncio
nest_asyncio.apply()

st.title('Streamlit App for Conversational PDF and CSV Interaction')

# Input for OpenAI API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

if api_key:
    openai.api_key = api_key

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

            # Save the dataframe as a string for interaction
            data_str = data.to_string()

            llm = OpenAI(model="gpt-3.5-turbo")

            def chat_with_data(data_str, query):
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"The following is a CSV data:\n{data_str}\n\nUser query: {query}\n\nAnswer:",
                    max_tokens=150
                )
                return response.choices[0].text.strip()

            user_query = st.text_input("Ask something about the data:")
            if user_query:
                response = chat_with_data(data_str, user_query)
                st.write(response)

    else:
        st.write("Please upload a CSV or PDF file to get started.")
else:
    st.write("Please enter your OpenAI API key to proceed.")

st.write("### Thank you for using this app!")
