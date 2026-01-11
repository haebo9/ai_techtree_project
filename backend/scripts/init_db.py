import sys
import os

# Backend root 경로를 path에 추가하여 app 모듈 import 가능하게 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
sys.path.append(backend_root)

from pymongo import ASCENDING, DESCENDING
from app.core.database import get_db

def init_db():
    print("🚀 Initializing Database Collections and Indexes...")
    
    db = get_db()
    
    # 1. Users Collections
    # Index: {"auth.email": 1} (Unique)
    # Index: {"auth.uid": 1}
    print("🔹 Setting up 'users' collection...")
    db.users.create_index([("auth.email", ASCENDING)], unique=True)
    db.users.create_index([("auth.uid", ASCENDING)])
    print("   - Created index: auth.email (Unique)")
    print("   - Created index: auth.uid")

    # 2. Interviews Collection
    # Index: {"user_id": 1}
    # Index: {"meta.status": 1}
    print("🔹 Setting up 'interviews' collection...")
    db.interviews.create_index([("user_id", ASCENDING)])
    db.interviews.create_index([("meta.status", ASCENDING)])
    print("   - Created index: user_id")
    print("   - Created index: meta.status")

    # 3. Tracks Collection
    # Index: {"title": 1} (Unique)
    print("🔹 Setting up 'tracks' collection...")
    db.tracks.create_index([("title", ASCENDING)], unique=True)
    print("   - Created index: title (Unique)")

    # 4. Trends Collection (Refactored)
    # Structure: TrendCategory (Grouped by category)
    # Index: {"category": 1} (Unique)
    # Index: {"items.link": 1} (For duplicate checking within category)
    print("🔹 Setting up 'trends' collection...")
    
    # Drop legacy indexes if needed (Manual intervention might be safer, but here we define the target state)
    # If standard indexes exist on 'category', create_index with unique=True might fail or convert depending on driver/version.
    # It is recommended to drop the 'trends' collection if the schema changed drastically.
    
    db.trends.create_index([("category", ASCENDING)], unique=True)
    db.trends.create_index([("items.link", ASCENDING)])
    db.trends.create_index([("items.tags", ASCENDING)])
    
    print("   - Created index: category (Unique)")
    print("   - Created index: items.link")
    print("   - Created index: items.tags")

    # 5. Questions Collection
    # Index: {"subject": 1, "level": 1}
    print("🔹 Setting up 'questions' collection...")
    db.questions.create_index([("subject", ASCENDING), ("level", ASCENDING)])
    print("   - Created index: subject + level")
    
    # 6. Concepts Collection
    # Index: {"subject": 1, "level": 1}
    # Index: {"name": 1}
    print("🔹 Setting up 'concepts' collection...")
    db.concepts.create_index([("subject", ASCENDING), ("level", ASCENDING)])
    db.concepts.create_index([("name", ASCENDING)])
    print("   - Created index: subject + level")
    print("   - Created index: name")

    print("\n✅ Database Initialization Completed!")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
