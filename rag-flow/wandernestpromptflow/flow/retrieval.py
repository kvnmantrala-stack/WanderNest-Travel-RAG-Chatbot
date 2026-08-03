from promptflow import tool
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from promptflow.connections import CognitiveSearchConnection


@tool
def retrieve_documents(
    query: str,
    search_connection: CognitiveSearchConnection,
    index_name: str,
    top_k: int = 3
) -> str:
    """
    Retrieve relevant document chunks from Azure AI Search.
    """

    if not query:
        return ""

    try:
        # Create Search Client
        search_client = SearchClient(
            endpoint=search_connection.api_base,
            index_name=index_name,
            credential=AzureKeyCredential(search_connection.api_key)
        )

        # Execute search
        results = search_client.search(
            search_text=query,
            top=top_k
        )

        docs = []

        for result in results:
            # Extract fields from your index
            content = result.get("chunk", "")
            source = result.get("title", "")

            if content:
                if source:
                    docs.append(
                        f"Source: {source}\n\n{content}"
                    )
                else:
                    docs.append(content)

        # Return combined retrieved content
        return "\n\n".join(docs)

    except Exception as e:
        print(f"Azure AI Search Error: {e}")
        return ""