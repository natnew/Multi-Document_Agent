import streamlit as st
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from utils import get_doc_tools

# Define URLs and papers
urls = [
    "https://openreview.net/pdf?id=VtmBAGCN7o",
    "https://openreview.net/pdf?id=6PmJoRfdaK",
    "https://openreview.net/pdf?id=hSyW5go0v8",
]

papers = [
    "metagpt.pdf",
    "longlora.pdf",
    "selfrag.pdf",
]

# Fetch tools for each paper
paper_to_tools_dict = {}
for paper in papers:
    st.write(f"Getting tools for paper: {paper}")
    vector_tool, summary_tool = get_doc_tools(paper, Path(paper).stem)
    paper_to_tools_dict[paper] = [vector_tool, summary_tool]

# Initialize tools and LLM
initial_tools = [t for paper in papers for t in paper_to_tools_dict[paper]]
llm = OpenAI(model="gpt-3.5-turbo")

# Create agent
agent_worker = FunctionCallingAgentWorker.from_tools(
    initial_tools, 
    llm=llm, 
    verbose=True
)
agent = AgentRunner(agent_worker)

# Streamlit app layout
st.title("Paper Analysis App")

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

# Run the app with `streamlit run app.py`
