import sys
import os
import logging
from datetime import datetime

# Add backend directory to path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import json

try:
    from app.core.database import mongodb
    # from app.source.track import AI_TECH_TREE # Removed
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TRACK_DB_PATH = os.path.join(os.path.dirname(__file__), "../app/source/tracks.json")

def _load_track_data():
    with open(TRACK_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def sync_tracks():
    """
    Synchronizes the AI_TECH_TREE data from python source to MongoDB 'tracks' collection.
    - Clears existing tracks to ensure source of truth is the code.
    - Transforms the nested dictionary structure into the DB dictionary format.
    - Handles the unified 'Option' structure.
    """
    logger.info("Connecting to Database...")
    try:
        mongodb.connect()
        db = mongodb.db
        if db is None:
            raise Exception("Database connection returned None")
    except Exception as e:
        logger.error(f"Failed to connect to DB: {e}")
        return

    collection = db['tracks']
    
    # 1. Clear existing tracks
    delete_result = collection.delete_many({})
    logger.info(f"Cleared {delete_result.deleted_count} existing tracks.")

    new_docs = []
    order_counter = 1

    # 2. Iterate and transform data
    # AI_TECH_TREE structure: Track -> Description/Steps -> Step -> Option -> Subject -> Levels
    
    ai_tech_tree = _load_track_data()
    for track_title, track_data in ai_tech_tree.items():
        logger.info(f"Processing {track_title}...")
        
        steps_doc = []
        # Sort steps by name to ensure consistent order (Step 1, Step 2, ...)
        sorted_step_keys = sorted(track_data["steps"].keys())
        
        for step_key in sorted_step_keys:
            step_content = track_data["steps"][step_key] # This is a Dict of Options
            
            options_doc = []
            
            # Sort options
            sorted_option_keys = sorted(step_content.keys())
            
            for opt_key in sorted_option_keys:
                opt_data = step_content[opt_key] # This is a Dict of Subjects
                
                subjects_doc = []
                # Sort subjects might not be strictly necessary but good for determinism
                # We assume subjects order in dict might matter or arbitrary. sorting by key for now.
                # Or if the user meant "Subjects" dict to be ordered... dicts are ordered in modern python.
                # Let's just iterate.
                
                for subject_title, levels in opt_data.items():
                    # Transform nested levels dict if needed, but schema says Dict[str, List[str]]
                    # track.py: "Lv1": [...]
                    # schema: levels: Dict[str, List[str]]
                    # It matches directly.
                    
                    subjects_doc.append({
                        "title": subject_title,
                        "levels": levels
                    })
                
                options_doc.append({
                    "option_name": opt_key,
                    "subjects": subjects_doc
                })
            
            # Determine type
            # If 1 option, we mark as FIXED, but we still populate 'options' list 
            # to maintain the "Unified Structure" requested by user in the DB as well.
            # Schema allows options list in TrackStep.
            step_type = "FIXED" if len(options_doc) == 1 else "BRANCH"
            
            steps_doc.append({
                "step_name": step_key,
                "type": step_type,
                "subjects": [], # We use options structure even for FIXED to be unified
                "options": options_doc
            })
            
        track_doc = {
            "title": track_title,
            "description": track_data["description"],
            "order": order_counter,
            "steps": steps_doc,
            "last_updated": datetime.utcnow()
        }
        new_docs.append(track_doc)
        order_counter += 1

    # 3. Insert new tracks
    if new_docs:
        result = collection.insert_many(new_docs)
        logger.info(f"✅ Successfully inserted {len(result.inserted_ids)} tracks.")
    else:
        logger.warning("No tracks found to insert.")

if __name__ == "__main__":
    sync_tracks()
