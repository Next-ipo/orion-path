import os
import re
import json
from datetime import datetime

# Path definition
BASE_DIR = r"h:\2nd-Brain"
LOG_DIR = os.path.join(BASE_DIR, "05_日誌")
PROJECT_DIR = os.path.join(BASE_DIR, r"01_プロジェクト\ippo-experience-hub")
DATA_FILE = os.path.join(PROJECT_DIR, r"data\dashboard.json")

def get_latest_log():
    # Only match standard daily notes like YYYY-MM-DD.md
    files = [f for f in os.listdir(LOG_DIR) if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f)]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(LOG_DIR, files[0])

def extract_data(log_path):
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading log: {e}")
        return None

    # Unicode escapes for Japanese keywords
    # ランク = \u30e9\u30f3\u30af
    # 最新状況 = \u6700\u65b0\u72b6\u6cc1
    
    # Extract Ippo Index
    ippo_pattern = r"\u30e9\u30f3\u30af\s+([A-Z])\*\*\s+\((\d+)\s+/\s+100\)"
    ippo_match = re.search(ippo_pattern, content)
    index_rank = ippo_match.group(1) if ippo_match else "N/A"
    index_score = ippo_match.group(2) if ippo_match else "0"

    # Extract Rocket Intelligence (Artemis II Status)
    rocket_status = "No updates."
    for line in content.splitlines():
        if "Artemis II" in line and "\u6700\u65b0\u72b6\u6cc1" in line:
            # We found the line. Now split by colon (half or full width)
            parts = re.split(r"[:：]", line, 1)
            if len(parts) > 1:
                # Clean up: strip markdown bolding and whitespace
                raw_status = parts[1].strip()
                # Remove trailing bold marks and whitespace
                rocket_status = re.sub(r"[\s\*]+$", "", raw_status).strip()
                break
    
    return {
        "date": datetime.now().strftime("%Y.%m.%d"),
        "starry_sky": {
            "rank": index_rank,
            "score": int(index_score)
        },
        "rocket": {
            "mission": "Artemis II",
            "status": rocket_status
        }
    }

def main():
    log_path = get_latest_log()
    if not log_path:
        print("No log found.")
        return

    print(f"Syncing from: {log_path}")
    data = extract_data(log_path)
    if not data:
        return
    
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully updated: {DATA_FILE}")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
