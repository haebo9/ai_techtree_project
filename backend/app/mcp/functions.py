import json
import os
import threading
import numpy as np
from datetime import datetime, timedelta
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient
from app.ai.source.track import AI_TECH_TREE

# ---------------------------------------------------------
# Global Configuration
# ---------------------------------------------------------
TREND_DB_PATH = "app/ai/source/trend.json"
MIN_MATCH_COUNT = 1   # Keywords match count to consider relevant

# Global instances (Lazily initialized)
EMBEDDING_MODEL = None
CHAT_MODEL = None  # Helper LLM for summarization
TAVILY_CLIENT = None
TRACK_EMBEDDINGS = {} # Cache for track embeddings

def _get_chat_model():
    """Lazily initialize Chat Model for summarization."""
    global CHAT_MODEL
    if CHAT_MODEL is None:
        try:
             api_key = os.environ.get("OPENAI_API_KEY")
             if not api_key:
                 raise ValueError("OpenAI API Key not found.")
             # Use a lightweight model for speed
             CHAT_MODEL = ChatOpenAI(model="gpt-5-nano", api_key=api_key, temperature=0.5)
        except Exception as e:
            print(f"Failed to initialize chat model: {e}")
            return None
    return CHAT_MODEL

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

# ---------------------------------------------------------
# Knowledge Base Management (Lightweight Text Matching)
# ---------------------------------------------------------

def _clean_text(text: str) -> str:
    """
    Cleans up raw text logic remains as basic fallback.
    """
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    return " ".join(text.split())

def _summarize_content(title: str, content: str) -> str:
    """
    Uses LLM to generate a clean, concise summary of the content.
    """
    llm = _get_chat_model()
    if not llm:
        return _clean_text(content)[:300] + "..." # Fallback
        
    try:
        prompt = PromptTemplate.from_template(
            """Summarize the following tech article content in 2-3 clear, informative sentences in Korean.
            Focus on the key technical insights or news.
            
            Title: {title}
            Content: {content}
            
            Summary:"""
        )
        chain = prompt | llm | StrOutputParser()
        # Limit content length to avoid exceeding context window for very long scrapes
        summary = chain.invoke({"title": title, "content": content[:3000]})
        return summary
    except Exception as e:
        print(f"Summarization failed: {e}")
        return _clean_text(content)[:300] + "..."

def _load_knowledge_base() -> list[dict]:
    """Loads trend data from JSON. (No embeddings, just text data)"""
    if not os.path.exists(TREND_DB_PATH):
        return []
    try:
        with open(TREND_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return []

def _save_knowledge_base(data: list[dict]):
    """Saves lightweight trend data."""
    try:
        os.makedirs(os.path.dirname(TREND_DB_PATH), exist_ok=True)
        with open(TREND_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving knowledge base: {e}")

def _process_and_save_background(results: list[dict], search_terms: list[str], category: str = "tech_news"):
    """
    Background Task:
    1. Clean content (No LLM summary to save cost).
    2. Save data to JSON with category info.
    """
    try:
        accumulated_items = []
        for res in results:
            # Cost Optimization: Use simple text cleaning instead of LLM
            clean_summary = _clean_text(res.get("content", ""))[:800] + "..."
            
            item = {
                "title": _clean_text(res.get("title")),
                "link": res.get("url"),
                "summary": clean_summary,
                "tags": search_terms,
                "category": category, # Add category metadata
                "collected_at": datetime.utcnow().isoformat()
            }
            accumulated_items.append(item)
            
        # Critical Section: Load -> Check -> Save
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
    Search First & Archive Strategy (Async):
    1. Select domains based on Category (tech_news, engineering, research, k_blog).
    2. Always perform a fresh Web Search.
    3. Return results IMMEDIATELY.
    4. Spawn a background thread to Archive to `trend.json` with Category tag.
    """
    client = _get_tavily_client()
    if not client:
        return [{"title": "System Error", "link": "", "summary": "Search client not available."}]

    # Normalize keywords for tagging
    search_terms = [k.lower().strip() for k in keywords if k.strip()]
    query_text = " ".join(keywords)
    # Refined Query: Ask for specific insights/trends to avoid generic homepage/wikipedia results
    if category == "k_blog":
         search_query = query_text # Trust the domain filter
    else:
         search_query = f"Latest technical trends, insights, and news about {query_text} in 2024-2025"
    
    # Domain Strategy based on Category
    DOMAIN_MAP = {
        "tech_news": [  
            "news.hada.io",                 # GeekNews (High Quality Curated)
            "news.ycombinator.com",         # Hacker News (글로벌)
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
            "velog.io"                      # Korean Dev Blogs (High Volume)
        ]
    }
    
    # Default to 'engineering' if invalid category
    target_domains = DOMAIN_MAP.get(category.lower(), DOMAIN_MAP["engineering"])
    
    try:
        # 1. Web Search (Targeted Level)
        response = client.search(
            query=search_query,
            search_depth="advanced", # tavily search option
            include_answer=False,
            max_results=5,
            include_domains=target_domains
        )
        
        results = response.get("results", [])
        
        # Fallback Strategy: If NO results in curated domains, try Global Search (Safe Fallback)
        if not results:
             print(f"[Fallback] No results in category '{category}'. Switching to global search.")
             # Remove domain restriction to find ANY relevant info
             fb_response = client.search(
                query=search_query, 
                search_depth="basic", # Use basic for speed in fallback
                include_answer=False,
                max_results=3,
                # include_domains is OMITTED here to search the entire web
            )
             results.extend(fb_response.get("results", []))

        # 2. Prepare Immediate Response for User (Fast)
        user_response_items = []
        for res in results:
            item = {
                "title": _clean_text(res.get("title")),
                "link": res.get("url"),
                "summary": _clean_text(res.get("content", ""))[:800] + "...", # Fast text slicing
                "tags": search_terms,
                "collected_at": datetime.utcnow().isoformat()
            }
            user_response_items.append(item)
            
        # 3. Spawn Background Thread for LLM Summarization & Saving
        # We pass the raw 'results' to the thread so it can do full processing
        thread = threading.Thread(target=_process_and_save_background, args=(results, search_terms, category))
        thread.start()
            
        return user_response_items[:5]

    except Exception as e:
        return [{"title": "Search Error", "link": "", "summary": str(e)}]


# ---------------------------------------------------------
# Track Recommendation Logic (Uses Embeddings)
# ---------------------------------------------------------

def _initialize_track_embeddings():
    """Lazily initializes embeddings for all tracks defined in AI_TECH_TREE."""
    if TRACK_EMBEDDINGS:
        return
    
    model = _get_embedding_model()
    if not model:
        return

    texts = []
    keys = []
    for track_name, track_data in AI_TECH_TREE.items():
        description = track_data.get("description", "")
        # Include Tier names and key topics
        tiers_content = []
        if "tiers" in track_data:
            for tier_name, tier_data in track_data["tiers"].items():
                tiers_content.append(tier_name)
        
        full_text = f"{track_name}. {description}. Key Areas: {', '.join(tiers_content)}"
        
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
    """Helper function to perform embedding similarity search for Tracks."""
    _initialize_track_embeddings()
    if not TRACK_EMBEDDINGS:
         return {"error": "Failed to initialize embeddings."}
         
    model = _get_embedding_model()
    if not model:
        return {"error": "Embedding model not initialized."}

    # Embed user query
    try:
        query_vector = model.embed_query(query_text)
    except Exception as e:
        return {"error": f"Embedding generation failed: {e}"}
    
    # Find best match
    best_track = None
    best_score = -1.0
    
    for track_name, track_vector in TRACK_EMBEDDINGS.items():
        score = _cosine_similarity(query_vector, track_vector)
        if score > best_score:
            best_score = score
            best_track = track_name
            
    return {"best_track": best_track, "score": best_score}
