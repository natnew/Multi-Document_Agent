from some_vector_library import SomeVectorTool
from some_summary_library import SomeSummaryTool

def get_doc_tools(paper, paper_name):
    vector_tool = SomeVectorTool(paper)
    summary_tool = SomeSummaryTool(paper)
    return vector_tool, summary_tool
