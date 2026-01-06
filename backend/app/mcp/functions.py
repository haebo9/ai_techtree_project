import numpy as np
from langchain_openai import OpenAIEmbeddings
from app.ai.source.topics import AI_TECH_TREE
import os
from tavily import TavilyClient

# ---------------------------------------------------------
# Global State & Configurations
# ---------------------------------------------------------
TRACK_EMBEDDINGS = {}
EMBEDDING_MODEL = None

def _get_embedding_model():
    """Lazily initialize Embedding Model."""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None:
        try:
             # Ensure dotenv is loaded if needed, or rely on execution context
             api_key = os.environ.get("OPENAI_API_KEY")
             if not api_key:
                 raise ValueError("OpenAI API Key not found.")
             EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize embedding model: {e}")
            return None
    return EMBEDDING_MODEL

def _initialize_track_embeddings():
    """
    Lazily initializes embeddings for all tracks defined in AI_TECH_TREE.
    This runs only once when called for the first time.
    """
    if TRACK_EMBEDDINGS:
        return
    
    model = _get_embedding_model()
    if not model:
        return

    texts = []
    keys = []
    
    # Construct descriptive text for each track to be embedded
    for track_name, track_data in AI_TECH_TREE.items():
        description = track_data.get("description", "")
        # Include Tier names and key topics to enhance semantic matching
        tiers_content = []
        if "tiers" in track_data:
            for tier_name, tier_data in track_data["tiers"].items():
                tiers_content.append(tier_name)
                # optionally add subject names if needed for deeper matching
        
        # Format: "Track Name. Description. Tiers: ..."
        full_text = f"{track_name}. {description}. Key Areas: {', '.join(tiers_content)}"
        
        texts.append(full_text)
        keys.append(track_name)
    
    # Batch embedding generation
    try:
        embeddings = model.embed_documents(texts)
        for key, vector in zip(keys, embeddings):
            TRACK_EMBEDDINGS[key] = vector
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Build dummy embeddings or handle failure appropriately for production

def _cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

def perform_search_similarity(query_text: str) -> dict:
    """Helper function to perform embedding similarity search."""
    # 1. Ensure embeddings are ready
    _initialize_track_embeddings()
    if not TRACK_EMBEDDINGS:
         return {"error": "Failed to initialize embeddings."}
         
    model = _get_embedding_model()
    if not model:
        return {"error": "Embedding model not initialized."}

    # 2. Embed user query
    try:
        query_vector = model.embed_query(query_text)
    except Exception as e:
        return {"error": f"Embedding generation failed: {e}"}
    
    # 3. Find best match
    best_track = None
    best_score = -1.0
    
    for track_name, track_vector in TRACK_EMBEDDINGS.items():
        score = _cosine_similarity(query_vector, track_vector)
        if score > best_score:
            best_score = score
            best_track = track_name
            
    return {"best_track": best_track, "score": best_score}

# Initialize Tavily Client
# NOTE: Ensure TAVILY_API_KEY is set in your environment variables.
try:
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
except Exception:
    tavily_client = None
    print("Warning: TAVILY_API_KEY not found. Search functionality will be limited.")

def perform_web_search(keywords: list[str]) -> list[dict]:
    """
    Performs a web search using Tavily API based on the provided keywords.
    """
    if not tavily_client:
         return [{"title": "Error", "link": "", "summary": "Search is unavailable. Please check TAVILY_API_KEY."}]

    # Construct a natural language query from keywords
    query = f"Latest AI trends and news about {' '.join(keywords)} technology in 2024-2025"
    
    try:
        # qna_search returns a direct answer, but we want search results. 
        # using .search() with search_depth="advanced" typically yields good results for trends.
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            include_answer=False,
            max_results=5
        )
        
        results = []
        for res in response.get("results", []):
            results.append({
                "title": res.get("title"),
                "link": res.get("url"),
                "summary": res.get("content")[:300] + "..." # Truncate summary
            })
        return results

    except Exception as e:
        return [{"title": "Search Error", "link": "", "summary": f"An error occurred during search: {e}"}]
