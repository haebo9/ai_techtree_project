from typing import List, Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from app.mcp.tools_functions import (
    f_get_techtree_track,
    f_get_techtree_path,
    f_get_techtree_trend,
    f_get_techtree_subject,
    f_get_techtree_survey
)
from app.mcp.tools_pydantic import (
    TrackOutput, 
    PathOutput, 
    TrendOutput, 
    SubjectOutput,
    SurveyOutput
)

# Initialize FastMCP Server
mcp = FastMCP("AI TechTree")

# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------
@mcp.tool()
def get_techtree_track(
    interests: Annotated[List[str], Field(description="List of keywords. Pass ['ALL'] to see all available tracks.")],
    experience_level: Annotated[str, Field(description="User's experience level ('beginner', 'intermediate', 'expert').")]
) -> TrackOutput:
    """
    Analyzes user interests to recommend a track, OR lists all available tracks.

    IMPORTANT FOR LLM:
    - **Trigger Condition**: Use this tool IMMEDIATELY when the user asks "What should I study?" or "What tracks are available?".
    - **From Survey**: If you have the result from `get_techtree_survey`, use the EXACT list of keywords from the user's selected interest option as the `interests` argument. (e.g. `interests=['llm', 'langchain', ...]`)
    - **Show All Tracks**: If the user asks for a list of tracks or is unsure, Call this tool with `interests=["ALL"]`.
    """
    data = f_get_techtree_track(interests, experience_level)
    return TrackOutput(**data)

@mcp.tool()
def get_techtree_path(
    track_name: Annotated[str, Field(description="Exact name of the track (e.g., 'Track 1: AI Engineer').")]
) -> PathOutput:
    """
    Retrieves the full hierarchical curriculum roadmap for a specific track.

    IMPORTANT FOR LLM:
    - Use this structured data to create a "Step-by-Step Learning Plan" for the user.
    - **Focus on Sequence**: Emphasize the logical order of study (Step 1 -> Step 2 -> Step 3).
    - Step 3 (Application) focuses on projects and specialized domains.
    - Do NOT suggest specific time durations (e.g., "2 weeks") unless explicitly asked. Focus on **what to learn first** and **why**.
    """
    data = f_get_techtree_path(track_name)
    return PathOutput(**data)


@mcp.tool()
def get_techtree_subject(
    subject_name: Annotated[str, Field(description="The exact name of the subject (e.g., 'Vector DB', 'Python Syntax').")]
) -> SubjectOutput:
    """
    Retrieves detailed learning concepts (Lv1, Lv2, Lv3) for a specific subject.
    Use this when the user asks for "What is X?", "What should I study in X?", or details about a specific roadmap item.
    """
    data = f_get_techtree_subject(subject_name)
    return SubjectOutput(**data)

@mcp.tool()
def get_techtree_trend(
    keywords: Annotated[List[str], Field(description="List of technical keywords (e.g., ['LLM', 'Agent', 'RAG']). Include 3-5 related keywords for better tagging.")],
    category: Annotated[str, Field(description="Target content category ('tech_news', 'engineering', 'research', 'k_blog').")] = "k_blog"
) -> TrendOutput:
    """
    Performs a web search to provide the latest AI trend, news, and GitHub repositories based on keywords.
    Uses Tavily Search API with category-based domain filtering.

    IMPORTANT FOR LLM: 
    - "tech_news": Global Tech News & Trend (English sources like GeekNews, HackerNews).
    - "k_blog": **ALL Korean Content** (Korean Tech Blogs, News, Industry Cases). Select this for ANY Korean query.
    - "engineering": Implementation details (GitHub, WandB, LangChain).
    - "research": Academic papers (Arxiv).
    """
    data = f_get_techtree_trend(keywords, category)
    return TrendOutput(**data)

@mcp.tool()
def get_techtree_survey() -> SurveyOutput:
    """
    Returns a simple survey to understand the user's development experience and AI interests.
    
    IMPORTANT FOR LLM:
    - **Trigger Condition**: Use this tool ONLY when you lack sufficient information about the user's **'experience_level'** OR **'interests'**.
    - **Do NOT use**: If the user has already explicitly stated their development experience (e.g., "I'm a senior dev") AND their specific area of interest (e.g., "I want to build chatbots"). In that case, proceed directly to `get_techtree_track`.
    - **Goal**: Collect missing metadata to provide accurate recommendations.
    """
    data = f_get_techtree_survey()
    return SurveyOutput(**data)


# No need to explicitly manually list MCP_TOOLS list if using @mcp.tool decorator with FastMCP's internal registry,
# but keeping it for reference if needed elsewhere. 
MCP_TOOLS = [
    get_techtree_track,
    get_techtree_path,
    get_techtree_subject,
    get_techtree_trend,
    get_techtree_survey,
]
