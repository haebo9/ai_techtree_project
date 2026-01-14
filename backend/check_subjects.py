
from app.mcp.tools_functions import _load_track_data

def list_subjects():
    data = _load_track_data()
    subjects = []
    for track_name, track_val in data.items():
        for step_name, step_val in track_val.get("steps", {}).items():
            for key, val in step_val.items():
                if isinstance(val, dict):
                    if "Lv1" in val: # It's a subject
                        subjects.append(key)
                    else: # It's a group
                        for sub_key, sub_val in val.items():
                            if isinstance(sub_val, dict) and "Lv1" in sub_val:
                                subjects.append(sub_key)
    print(f"Total subjects: {len(subjects)}")
    print(subjects[:10])

if __name__ == "__main__":
    list_subjects()
