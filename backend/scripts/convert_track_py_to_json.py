import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

try:
    from app.source.track import AI_TECH_TREE
except ImportError:
    print("Could not import AI_TECH_TREE.")
    sys.exit(1)

output_path = os.path.join(os.path.dirname(__file__), "../app/source/track.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(AI_TECH_TREE, f, indent=4, ensure_ascii=False)

print(f"Created {output_path}")
