import numpy as np
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.mcp.tools_functions import perform_web_search, recommend_ai_track, get_roadmap_details
from app.ai.source.track import AI_TECH_TREE

# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------

@tool
def get_ai_track(interests: List[str], experience_level: str) -> Dict[str, Any]:
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

@tool
def get_ai_path(track_name: str) -> Dict[str, Any]:
    """
    Retrieves the full hierarchical curriculum roadmap for a specific track.
    
    Args:
        track_name: Exact name of the track (e.g., "Track 1: AI Engineer").
        
    Returns:
        Dictionary containing the full structured roadmap (Tiers -> Subjects).
        
    IMPORTANT FOR LLM:
        - Use this structured data to create a "Step-by-Step Learning Plan" for the user.
        - **Focus on Sequence**: Emphasize the logical order of study (Tier 1 -> Tier 2 -> Tier 3).
        - Tier 3 (Application) focuses on projects and specialized domains.
        - Do NOT suggest specific time durations (e.g., "2 weeks") unless explicitly asked. Focus on **what to learn first** and **why**.
    """
    return get_roadmap_details(track_name)

@tool
def get_ai_trend(keywords: List[str], category: str = "tech_news") -> List[Dict[str, str]]:
    """
    Performs a web search to provide the latest AI trend, news, and GitHub repositories based on keywords.
    Uses Tavily Search API with category-based domain filtering.
    
    Args:
        keywords (List[str]): List of technical keywords (e.g., ["LLM", "Agent", "RAG"]). Include 3-5 related keywords for better tagging.
        category (str): Target content category ("tech_news", "engineering", "research", "k_blog").
        
    Returns:
        List[Dict[str, str]]: List of dictionaries with trend title, link, and summary.

    IMPORTANT FOR LLM: 
    - "tech_news": Global Tech News & Trend (English sources like GeekNews, HackerNews).
    - "k_blog": **ALL Korean Content** (Korean Tech Blogs, News, Industry Cases). Select this for ANY Korean query.
    - "engineering": Implementation details (GitHub, WandB, LangChain).
    - "research": Academic papers (Arxiv).
    """
    return perform_web_search(keywords, category)

MCP_TOOLS = [get_ai_track, get_ai_path, get_ai_trend]
