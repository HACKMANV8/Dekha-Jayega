from pathlib import Path
from datetime import datetime
from typing_extensions import Annotated, List, Literal, Dict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model 
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolArg
from Research.prompts import summarize_webpage_prompt
from tavily import TavilyClient
from Research.state_research import Summary
load_dotenv()
from datetime import datetime

def get_today_str():
    # This works on Windows
    return datetime.now().strftime("%a %b %#d, %Y")

def get_current_dir() -> Path:
    """Get the current directory of the module.

    This function is compatible with Jupyter notebooks and regular Python scripts.

    Returns:
        Path object representing the current directory
    """
    try:
        return Path(__file__).resolve().parent
    except NameError:  # __file__ is not defined
        return Path.cwd()

summarization_model = init_chat_model(model="gemini-2.5-flash")
tavily_client = TavilyClient()

def tavily_search_multiple(search_query: List[str], limit: int = 1, topic: Literal["general", "news", "science", "technology", "health", "sports", "entertainment", "business", "finance", "education", "politics", "world", "local"] = "general",include_raw_content: bool = True,) -> List[Dict]:
    """Search the web for multiple queries and return the results.

    Args:
        search_query: List of search queries to perform.
        limit: Maximum number of results to return for each query.
        topic: Topic of the search.
        include_raw_content: Whether to include the raw content of the search results.

    Returns:
        List of search results.
    """
    search_results = []
    for query in search_query:
        result = tavily_client.search(query, limit=limit, topic=topic, include_raw_content=include_raw_content)
        search_results.append(result)
    return search_results

def summarize_webpage(webpage_content: str) -> str:
    """Summarize the content of a webpage.

    Args:
        webpage_content: Content of the webpage to summarize.

    Returns:
        Summary of the webpage content.
    """
    try:
        structured_llm = summarization_model.with_structured_output(Summary)

        summary = structured_llm.invoke([
            HumanMessage(content=summarize_webpage_prompt.format(webpage_content=webpage_content,date=get_today_str()))
        ])
        

        formatted_summary = (
            f"<summary>\n{summary.summary}\n</summary>\n\n"
            f"<key_excerpts>\n{summary.key_excerpts}\n</key_excerpts>"
        )

        return formatted_summary

    except Exception as e:
        print(f"Error summarizing webpage: {e}")
        return webpage_content[:1000] + "..." if len(webpage_content) > 1000 else webpage_content

def deduplicate_search_results(search_results: List[Dict]) -> dict:
    """Deduplicate search results based on the title and url.

    Args:
        search_results: List of search results dictionaries.

    Returns:
        Dictionary mapping URLs to unique results
    """
    unique_results = {}

    for response in search_results:
        for result in response["results"]:
            url = result["url"]
            if url not in unique_results:
                unique_results[url] = result
    
    return unique_results

def process_search_results(unique_results: dict) -> dict:
    """Process the search results and return the formatted summary.

    Args:
        unique_results: Dictionary mapping URLs to unique results.

    Returns:
        Dictionary mapping URLs to formatted summaries.
    """
    summarized_results = {}
    
    for url, result in unique_results.items():
        # Use existing content if no raw content for summarization
        if not result.get("raw_content"):
            content = result['content']
        else:
            # Summarize raw content for better processing
            content = summarize_webpage(result['raw_content'])
        
        summarized_results[url] = {
            'title': result['title'],
            'content': content
        }
    
    return summarized_results

def format_search_results(summarized_results: dict) -> str:
    """Format the search results into a well-structured string output.

    Args:
        summarized_results: Dictionary mapping URLs to formatted summaries.

    Returns:
        formatted string of search results with clear source seperation.
    """
    if not summarized_results:
        return "No valid search results found. Please try different search queries or use a different search API."
    
    formatted_output = "Search results: \n\n"
    
    for i, (url, result) in enumerate(summarized_results.items(), 1):
        formatted_output += f"\n\n--- SOURCE {i}: {result['title']} ---\n"
        formatted_output += f"URL: {url}\n\n"
        formatted_output += f"SUMMARY:\n{result['content']}\n\n"
        formatted_output += "-" * 80 + "\n"
    
    return formatted_output


#tools

@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 1,
    topic: Annotated[Literal["general", "news", "finance"], InjectedToolArg] = "general",
) -> str:
    """Fetch results from Tavily search API with content summarization.

    Args:
        query: A single search query to execute
        max_results: Maximum number of results to return
        topic: Topic to filter results by ('general', 'news', 'finance')

    Returns:
        Formatted string of search results with summaries
    """
    # Execute search for single query
    search_results = tavily_search_multiple(
        [query],  # Convert single query to list for the internal function
        limit=max_results,
        topic=topic,
        include_raw_content=True,
    )

    unique_results = deduplicate_search_results(search_results)

    summarized_results = process_search_results(unique_results)

    return format_search_results(summarized_results)

@tool
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.
    
    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.
    
    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    
    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?
    
    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps
        
    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"