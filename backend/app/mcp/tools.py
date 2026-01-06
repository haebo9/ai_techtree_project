import numpy as np
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.mcp.functions import perform_search_similarity, perform_web_search
from app.ai.source.topics import AI_TECH_TREE

# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------

@tool
def get_ai_track(interests: List[str], experience_level: str) -> Dict[str, Any]:
    """
    Analyzes user interests and experience to recommend the most suitable AI track using Semantic Search.
    The tool compares the semantic meaning of the user's interests with the curriculum descriptions.
    
    Args:
        interests: List of interest keywords (e.g., ["web", "backend", "system design"]).
        experience_level: User's experience level ("beginner", "intermediate", "expert").
        
    Returns:
        Dictionary containing recommended track, match reason, and starting point.
    """
    query_text = " ".join(interests)
    result = perform_search_similarity(query_text)
    
    if "error" in result:
        return result
        
    best_track = result.get("best_track")
    best_score = result.get("score")

    # 4. Construct result
    if best_track:
        track_info = AI_TECH_TREE[best_track]
        
        # Determine starting point based on experience
        tiers = list(track_info.get("tiers", {}).keys())
        starting_point = tiers[0] if tiers else "Basis"
        
        if experience_level.lower() == "intermediate" and len(tiers) > 1:
            starting_point = tiers[1]
        elif experience_level.lower() == "expert" and len(tiers) > 2:
            starting_point = tiers[2]

        return {
            "recommended_track": best_track,
            "description": track_info.get("description", ""),
            "matching_score": round(float(best_score), 2),
            "reason": f"Your interests in '{', '.join(interests)}' match this track's focus on {track_info.get('description', '')}.",
            "starting_point": starting_point
        }
    else:
        return {"error": "No suitable track found."}

@tool
def get_ai_path(track_name: str) -> Dict[str, Any]:
    """
    Retrieves the full curriculum roadmap for a specific track, sorted in learning order.
    
    Args:
        track_name: Exact name of the track (e.g., "Track 1: AI Engineer").
        
    Returns:
        Dictionary containing the full roadmap of subjects.
    """
    track_data = AI_TECH_TREE.get(track_name)
    if not track_data:
        return {"error": f"Track '{track_name}' not found."}
    
    # Extract linear list of all subjects in the track
    all_subjects = []
    tiers = track_data.get("tiers", {})
    for tier_name, tier_content in tiers.items():
        # tier_content keys are Subject names (or Option categories)
        # Simplified traversal
        for key, val in tier_content.items():
            if "Lv1" in val: # It's a Subject
                all_subjects.append(key)
            else: # It might be an Option group or nested structure
                for sub_key, sub_val in val.items():
                     if isinstance(sub_val, dict) and "Lv1" in sub_val:
                         all_subjects.append(sub_key)
    
    return {
        "track": track_name,
        "total_subjects": len(all_subjects),
        "roadmap": all_subjects
    }

@tool
def get_ai_trend(keywords: List[str], category: str = "tech_news") -> List[Dict[str, str]]:
    """
    Performs a web search to provide the latest AI trend, news, and GitHub repositories based on keywords.
    Uses Tavily Search API with category-based domain filtering.
    
    Args:
        keywords: List of technical keywords (e.g., ["LLM", "Agent", "RAG"]). Include 3-5 related keywords for better tagging.
        category: Target content category ("tech_news", "engineering", "research", "k_blog"). Defaults to "tech_news".
               - tech_news: Global Tech News & Trend (English sources like GeekNews, HackerNews).
               - k_blog: **ALL Korean Content** (Korean Tech Blogs, News, Industry Cases). Select this for ANY Korean query.
               - engineering: Implementation details (GitHub, WandB, LangChain).
               - research: Academic papers (Arxiv).
        
    Returns:
        List of dictionaries with trend title, link, and summary.
    """
    return perform_web_search(keywords, category)

MCP_TOOLS = [get_ai_track, get_ai_path, get_ai_trend]
