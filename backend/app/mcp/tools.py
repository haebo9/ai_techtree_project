import numpy as np
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.mcp.tools_functions import perform_search_similarity, perform_web_search
from app.ai.source.track import AI_TECH_TREE

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

    IMPORTANT FOR LLM:
    - **Trigger Condition**: Use this tool IMMEDIATELY when the user asks "What should I study?", "Where do I start?", or "Recommend a path".
    - **Missing Info Handling**: If the user hasn't provided specific interests yet:
      1. You may call this tool with broad keywords like ["AI Foundation", "General"] and experience_level="beginner" to provide an initial suggestion.
      2. OR you can ask the user for their specific interests to narrow it down.
    - **Goal**: Always base your recommendations on the data returned by this tool, not your internal knowledge.
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
    Retrieves the full hierarchical curriculum roadmap for a specific track.
    
    Args:
        track_name: Exact name of the track (e.g., "Track 1: AI Engineer").
        
    Returns:
        Dictionary containing the full structured roadmap (Tiers -> Subjects).
        
    IMPORTANT FOR LLM:
        - Use this structured data to create a "Step-by-Step Learning Plan" for the user.
        - **Focus on Sequence**: Emphasize the logical order of study (Tier 1 -> Tier 2 -> Tier 3).
        - Tier 1 (Basis) is the mandatory foundation. Start here.
        - Tier 2 (Core) contains the most critical skills.
        - Tier 3 (Application) focuses on projects and specialized domains.
        - Do NOT suggest specific time durations (e.g., "2 weeks") unless explicitly asked. Focus on **what to learn first** and **why**.
    """
    track_data = AI_TECH_TREE.get(track_name)
    if not track_data:
        return {"error": f"Track '{track_name}' not found."}
    
    # Reconstruct hierarchy for better LLM Understanding
    roadmap_structure = {}
    tiers = track_data.get("tiers", {})
    
    for tier_name, tier_content in tiers.items():
        roadmap_structure[tier_name] = []
        
        for key, val in tier_content.items():
            if "Lv1" in val: # It's a Subject
                subject_info = {
                    "subject": key,
                    "description": val.get("desc", ""),
                    "importance": "High"  # Subjects directly under Tier are usually core
                }
                roadmap_structure[tier_name].append(subject_info)
            else: # It's a Group/Option
                for sub_key, sub_val in val.items():
                     if isinstance(sub_val, dict) and "Lv1" in sub_val:
                         subject_info = {
                            "subject": sub_key,
                            "category": key, # Group name (e.g., "Language")
                            "description": sub_val.get("desc", ""),
                            "importance": "Medium"
                        }
                         roadmap_structure[tier_name].append(subject_info)
    
    return {
        "track": track_name,
        "description": track_data.get("description"),
        "roadmap": roadmap_structure
    }

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
