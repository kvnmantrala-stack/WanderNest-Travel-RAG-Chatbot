from promptflow import tool

@tool
def retrieve_documents(
    query: str,
    search_connection,
    index_name: str,
    top_k: int = 3
) -> str:
    return "THIS IS THE LATEST RETRIEVAL.PY"