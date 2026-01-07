import json
import os
import threading
import numpy as np
from datetime import datetime
from urllib.parse import urlparse
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient
from app.ai.source.track import AI_TECH_TREE

# =========================================================
# 1. Global Configuration & Lazy Loaders
# =========================================================

TREND_DB_PATH = "app/ai/source/trend.json"
MIN_MATCH_COUNT = 1 

# Global instances
EMBEDDING_MODEL = None
TAVILY_CLIENT = None
TRACK_EMBEDDINGS = {} 

def _get_embedding_model():
    """Lazily initialize Embedding Model (Only for Track Search)."""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None:
        try:
             api_key = os.environ.get("OPENAI_API_KEY")
             if not api_key:
                 raise ValueError("OpenAI API Key not found.")
             EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize embedding model: {e}")
            return None
    return EMBEDDING_MODEL

def _get_tavily_client():
    """Lazily initialize Tavily Client."""
    global TAVILY_CLIENT
    if TAVILY_CLIENT is None:
        try:
            api_key = os.environ.get("TAVILY_API_KEY")
            if api_key:
                TAVILY_CLIENT = TavilyClient(api_key=api_key)
            else:
                print("Warning: TAVILY_API_KEY not found.")
        except Exception as e:
            print(f"Failed to initialize Tavily client: {e}")
    return TAVILY_CLIENT


# =========================================================
# 2. Shared Utilities
# =========================================================

def _extract_domain(url: str) -> str:
    """Extracts simplified domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")
    except:
        return ""

def _clean_text(text: str) -> str:
    """Basic text cleaning."""
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    return " ".join(text.split())


# =========================================================
# 3. Core Logic: Web Search (get_ai_trend)
# =========================================================

def _load_knowledge_base() -> list[dict]:
    """Loads trend data from JSON."""
    if not os.path.exists(TREND_DB_PATH):
        return []
    try:
        with open(TREND_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return []

def _save_knowledge_base(data: list[dict]):
    """Saves trend data to JSON."""
    try:
        os.makedirs(os.path.dirname(TREND_DB_PATH), exist_ok=True)
        with open(TREND_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving knowledge base: {e}")

def _process_and_save_background(results: list[dict], search_terms: list[str], category: str = "tech_news"):
    """Background Task: Clean content and save to JSON archive."""
    try:
        accumulated_items = []
        for res in results:
            clean_summary = _clean_text(res.get("content", ""))[:800] + "..."
            
            item = {
                "title": _clean_text(res.get("title")),
                "link": res.get("url"),
                "summary": clean_summary,
                "tags": search_terms,
                "category": category,
                "collected_at": datetime.utcnow().isoformat()
            }
            accumulated_items.append(item)
            
        all_knowledge = _load_knowledge_base()
        existing_links = {item["link"] for item in all_knowledge}
        added_count = 0
        
        for item in accumulated_items:
            if item["link"] not in existing_links:
                all_knowledge.append(item)
                added_count += 1
        
        if added_count > 0:
            _save_knowledge_base(all_knowledge)
            
    except Exception as e:
        print(f"[Async] Background save failed: {e}")

def perform_web_search(keywords: list[str], category: str = "tech_news") -> list[dict]:
    """
    Executes web search using Tavily with domain filtering and background archiving.
    """
    client = _get_tavily_client()
    if not client:
        return [{"title": "System Error", "link": "", "summary": "Search client not available."}]

    # Normalize keywords
    search_terms = [k.lower().strip() for k in keywords if k.strip()]
    query_text = " ".join(keywords)
    
    if category == "k_blog":
         search_query = query_text
    else:
         search_query = f"Latest technical trends, insights, and news about {query_text} in 2024-2025"
    
    # Domain Filtering Configuration
    DOMAIN_MAP = {
        "tech_news": [  
            "news.hada.io",                 # GeekNews (High Quality Curated)
        ],
        "engineering": [
            "github.com",                   # Open Source
            "huggingface.co",               # AI Models & Papers
            "openai.com",                   # Official Blog
            "anthropic.com",                # Official Blog
            "langchain.com/blog",           # AI 앱 개발 메타
            "wandb.ai/fully-connected",     # 실무 엔지니어링
            "pytorch.org/blog",             # Official Framework Blog
        ],
        "research": [   
            "arxiv.org",                    # Research Papers
            "paperswithcode.com",           # Papers + Code
            "deepmind.google/research",     # DeepMind Research
            "research.google",              # Google Research
            "scholar.google.com",           # Google Scholar
            "openreview.net"                # Academic Reviews
        ],
        "k_blog": [      
            "techblog.woowahan.com",        # Woowa Bros
            "medium.com/daangn",            # Daangn Market
            "toss.tech",                    # Toss
            "devocean.sk.com",              # SK
            "helloworld.kurly.com",         # Kurly
            "techblog.lycorp.co.jp/ko",     # LINE
            "d2.naver.com",                 # Naver D2
            "kakaoenterprise.com",          # Kakao Enterprise
            "hyperconnect.com",             # Hyperconnect
            "ridicorp.com/story",           # Ridi
            "netmarble.engineering",        # Netmarble
        ]
    }
    
    target_domains = DOMAIN_MAP.get(category.lower(), DOMAIN_MAP["engineering"])
    
    try:
        # 1. Main Search
        response = client.search(
            query=search_query,
            search_depth="advanced",
            include_answer=False,
            max_results=5,
            include_domains=target_domains
        )
        
        results = response.get("results", [])
        
        # 2. Fallback Search (Global)
        if not results:
             print(f"[Fallback] No results in category '{category}'. Switching to global search.")
             fb_response = client.search(
                query=search_query, 
                search_depth="basic",
                include_answer=False,
                max_results=3
            )
             results.extend(fb_response.get("results", []))

        # 3. Format Response
        user_response_items = []
        for res in results:
            domain = _extract_domain(res.get("url", ""))
            clean_title = _clean_text(res.get("title"))
            final_title = f"{clean_title} | {domain}" if domain else clean_title

            item = {
                "title": final_title,
                "link": res.get("url"),
                "summary": _clean_text(res.get("content", ""))[:800] + "...",
                "tags": search_terms,
                "collected_at": datetime.utcnow().isoformat()
            }
            user_response_items.append(item)
            
        # 4. Background Archiving
        thread = threading.Thread(target=_process_and_save_background, args=(results, search_terms, category))
        thread.start()
            
        return user_response_items[:5]

    except Exception as e:
        return [{"title": "Search Error", "link": "", "summary": str(e)}]


# =========================================================
# 4. Core Logic: Track Recommendation (get_ai_track)
# =========================================================

def _initialize_track_embeddings():
    """Lazily initializes embeddings for all tracks."""
    if TRACK_EMBEDDINGS:
        return
    
    model = _get_embedding_model()
    if not model:
        return

    texts = []
    keys = []
    for track_name, track_data in AI_TECH_TREE.items():
        description = track_data.get("description", "")
        # Include Step names to enhance context
        steps_content = []
        if "steps" in track_data:
            for step_name in track_data["steps"].keys():
                steps_content.append(step_name)
        
        full_text = f"{track_name}. {description}. Key Areas: {', '.join(steps_content)}"
        texts.append(full_text)
        keys.append(track_name)
    
    try:
        embeddings = model.embed_documents(texts)
        for key, vector in zip(keys, embeddings):
            TRACK_EMBEDDINGS[key] = vector
    except Exception as e:
        print(f"Error generating embeddings: {e}")

def _cosine_similarity(vec_a, vec_b):
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm_a * norm_b)

def perform_search_similarity(query_text: str) -> dict:
    """Finds best matching track using embedding similarity."""
    _initialize_track_embeddings()
    if not TRACK_EMBEDDINGS:
         return {"error": "Failed to initialize embeddings."}
         
    model = _get_embedding_model()
    if not model:
        return {"error": "Embedding model not initialized."}

    try:
        query_vector = model.embed_query(query_text)
    except Exception as e:
        return {"error": f"Embedding generation failed: {e}"}
    
    best_track = None
    best_score = -1.0
    
    for track_name, track_vector in TRACK_EMBEDDINGS.items():
        score = _cosine_similarity(query_vector, track_vector)
        if score > best_score:
            best_score = score
            best_track = track_name
            
    return {"best_track": best_track, "score": best_score}

def recommend_ai_track(interests: list[str], experience_level: str) -> dict:
    """
    Main logic for 'get_ai_track'.
    Handles both 'list all' requests and semantic search recommendations.
    """
    # 0. Check for "List All" request
    check_keywords = {k.upper() for k in interests}
    if any(k in check_keywords for k in ["ALL", "LIST", "TRACKS", "전체", "목록"]) or not interests:
        all_tracks = []
        for name, data in AI_TECH_TREE.items():
            all_tracks.append({
                "track_name": name,
                "description": data.get("description", "")
            })
        return {"available_tracks": all_tracks, "message": "Here are all the available AI Tech Tracks."}

    # 1. Semantic Search
    query_text = " ".join(interests)
    result = perform_search_similarity(query_text)
    
    if "error" in result:
        return result
        
    best_track = result.get("best_track")
    best_score = result.get("score")

    # 2. Construct detailed result
    if best_track:
        track_info = AI_TECH_TREE[best_track]
        
        # Determine starting point based on experience
        steps = list(track_info.get("steps", {}).keys())
        starting_point = steps[0] if steps else "Basis"
        
        if experience_level.lower() == "intermediate" and len(steps) > 1:
            starting_point = steps[1]
        elif experience_level.lower() == "expert" and len(steps) > 2:
            starting_point = steps[2]

        return {
            "recommended_track": best_track,
            "description": track_info.get("description", ""),
            "matching_score": round(float(best_score), 2),
            "reason": f"Your interests in '{', '.join(interests)}' match this track's focus on {track_info.get('description', '')}.",
            "starting_point": starting_point
        }
    else:
        return {"error": "No suitable track found."}


# =========================================================
# 5. Core Logic: Roadmap Details (get_ai_path)
# =========================================================

def get_roadmap_details(track_name: str) -> dict:
    """
    Main logic for 'get_ai_path'.
    Retrieves and structures the full roadmap for a specific track.
    """
    track_data = AI_TECH_TREE.get(track_name)
    if not track_data:
        return {"error": f"Track '{track_name}' not found. Please provide exact track name."}
    
    # Reconstruct hierarchy for better LLM Understanding
    roadmap_structure = {}
    steps = track_data.get("steps", {})
    
    for step_name, step_content in steps.items():
        roadmap_structure[step_name] = []
        
        for key, val in step_content.items():
                # Check if it's a direct Subject (Level 1)
            if isinstance(val, dict) and "Lv1" in val:
                subject_info = {
                    "subject": key,
                    # "description": val.get("desc", ""), # Reduced for token efficiency
                    "importance": "High"
                }
                roadmap_structure[step_name].append(subject_info)
            else: 
                # It's a Group/Option (Nested)
                for sub_key, sub_val in val.items():
                     if isinstance(sub_val, dict) and "Lv1" in sub_val:
                         subject_info = {
                            "subject": sub_key,
                            "category": key, # e.g. "Language"
                            # "description": sub_val.get("desc", ""), # Reduced for token efficiency
                            "importance": "Medium"
                        }
                         roadmap_structure[step_name].append(subject_info)
    
    return {
        "track": track_name,
        "description": track_data.get("description"),
        "roadmap": roadmap_structure,
        "note": "Use 'get_techtree_detail' for specific subject details."
    }

def get_subject_details(subject_name: str) -> dict:
    """
    Finds detailed concepts (Lv1, Lv2, Lv3) for a specific subject across all tracks.
    Used by 'get_techtree_detail'.
    """
    # Normalize query
    query = subject_name.lower().strip()
    
    for track_name, track_val in AI_TECH_TREE.items():
        for step_name, step_val in track_val.get("steps", {}).items():
            
            for key, val in step_val.items():
                if not isinstance(val, dict): continue

                # 1. Direct Match (Subject Key)
                if key.lower() == query:
                     return {
                         "subject": key,
                         "track": track_name,
                         "details": val
                     }
                
                # 2. Nested Match (Inside Group/Option)
                for sub_key, sub_val in val.items():
                    if isinstance(sub_val, dict) and sub_key.lower() == query:
                        return {
                            "subject": sub_key,
                            "track": track_name,
                            "category": key,
                            "details": sub_val
                        }
                            
    return {"error": f"Subject '{subject_name}' not found. Please check the exact name from the roadmap."}
