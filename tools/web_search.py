
from tavily import TavilyClient
from langchain.tools import tool
import os


tavily_client = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for evidence related to a claim.
    """

    results = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    formatted = []

    for r in results["results"]:

        formatted.append(
            f"""
            TITLE: {r.get("title")}
            URL: {r.get("url")}
            CONTENT: {r.get("content")}
            """
        )

    return "\n\n".join(formatted)