from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from app.mcp.tools_functions import perform_web_search, recommend_ai_track, get_roadmap_details, get_subject_details

# Initialize FastMCP Server
mcp = FastMCP("AI TechTree")

# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------

@mcp.tool()
def get_techtree_track(interests: List[str], experience_level: str) -> Dict[str, Any]:
    """
    Analyzes user interests to recommend a track, OR lists all available tracks.
    
    Args:
        interests: List of keywords. Pass ["ALL"] to see all available tracks.
        experience_level: User's experience level ("beginner", "intermediate", "expert").
        
    Returns:
        Recommendation result OR list of all tracks.

    IMPORTANT FOR LLM:
    - **Trigger Condition**: Use this tool IMMEDIATELY when the user asks "What should I study?" or "What tracks are available?".
    - **Show All Tracks**: If the user asks for a list of tracks or is unsure, Call this tool with `interests=["ALL"]`.
    """
    return recommend_ai_track(interests, experience_level)

@mcp.tool()
def get_techtree_path(track_name: str) -> Dict[str, Any]:
    """
    Retrieves the full hierarchical curriculum roadmap for a specific track.
    
    Args:
        track_name: Exact name of the track (e.g., "Track 1: AI Engineer").
        
    Returns:
        Dictionary containing the full structured roadmap (Steps -> Subjects).
        
    IMPORTANT FOR LLM:
        - Use this structured data to create a "Step-by-Step Learning Plan" for the user.
        - **Focus on Sequence**: Emphasize the logical order of study (Step 1 -> Step 2 -> Step 3).
        - Step 3 (Application) focuses on projects and specialized domains.
        - Do NOT suggest specific time durations (e.g., "2 weeks") unless explicitly asked. Focus on **what to learn first** and **why**.
    """
    return get_roadmap_details(track_name)

@mcp.tool()
def get_techtree_trend(keywords: List[str], category: str = "k_blog") -> List[Dict[str, str]]:
    """
    Performs a web search to provide the latest AI trend, news, and GitHub repositories based on keywords.
    Uses Tavily Search API with category-based domain filtering.
    
    Args:
        keywords: List of technical keywords (e.g., ["LLM", "Agent", "RAG"]). Include 3-5 related keywords for better tagging.
        category: Target content category ("tech_news", "engineering", "research", "k_blog").
        
    Returns:
        List of dictionaries with trend title, link, and summary.

    IMPORTANT FOR LLM: 
    - "tech_news": Global Tech News & Trend (English sources like GeekNews, HackerNews).
    - "k_blog": **ALL Korean Content** (Korean Tech Blogs, News, Industry Cases). Select this for ANY Korean query.
    - "engineering": Implementation details (GitHub, WandB, LangChain).
    - "research": Academic papers (Arxiv).
    """
    return perform_web_search(keywords, category)

@mcp.tool()
def get_techtree_detail(subject_name: str) -> Dict[str, Any]:
    """
    Retrieves detailed learning concepts (Lv1, Lv2, Lv3) for a specific subject.
    Use this when the user asks for "What is X?", "What should I study in X?", or details about a specific roadmap item.
    
    Args:
        subject_name: The exact name of the subject (e.g., "Vector DB", "Python Syntax").
    """
    return get_subject_details(subject_name)

MCP_TOOLS = [
    get_techtree_track,
    get_techtree_path,
    get_techtree_trend,
    get_techtree_detail
]