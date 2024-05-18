import streamlit as st
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from utils import get_doc_tools

# Function to process uploaded files and URLs
def process_papers(files, urls):
    paper_to_tools_dict = {}
    for file in files:
        paper_name = file.name
        st.write(f"Getting tools for paper: {paper_name}")
        with open(paper_name, "wb") as f:
            f.write(file.getbuffer())
        vector_tool, summary_tool = get_doc_tools(paper_name, Path(paper_name).stem)
        paper_to_tools_dict[paper_name] = [vector_tool, summary_tool]
    for url in urls:
        paper_name = url.split("/")[-1] + ".pdf"
        st.write(f"Getting tools for paper from URL: {url}")
        # Here you need to download the file from URL and save it locally
        # This requires additional code to handle URL fetching
        # Example:
        # response = requests.get(url)
        # with open(paper_name, "wb") as f:
        #     f.write(response.content)
        vector_tool, summary_tool = get_doc_tools(paper_name, Path(paper_name).stem)
        paper_to_tools_dict[paper_name] = [vector_tool, summary_tool]
    return paper_to_tools_dict

# Streamlit app layout
st.title("Paper Analysis App")

uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])
url_input = st.text_area("Enter URLs of papers (one per line)")

if st.button("Process Papers"):
    urls = url_input.splitlines()
    paper_to_tools_dict = process_papers(uploaded_files, urls)
    
    # Initialize tools and LLM
    initial_tools = [t for paper in paper_to_tools_dict for t in paper_to_tools_dict[paper]]
    llm = OpenAI(model="gpt-3.5-turbo")
    
    # Create agent
    agent_worker = FunctionCallingAgentWorker.from_tools(
        initial_tools, 
        llm=llm, 
        verbose=True
    )
    agent = AgentRunner(agent_worker)

    # Queries input
    query1 = st.text_input("Enter your first query:", 
                           "Tell me about the evaluation dataset used in LongLoRA, and then tell me about the evaluation results")
    query2 = st.text_input("Enter your second query:", 
                           "Give me a summary of both Self-RAG and LongLoRA")

    if st.button("Run Queries"):
        response1 = agent.query(query1)
        response2 = agent.query(query2)
        
        st.subheader("Response to First Query")
        st.write(str(response1))
        
        st.subheader("Response to Second Query")
        st.write(str(response2))
