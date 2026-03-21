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

def md_to_html(md_text):
    """Simple markdown to HTML converter for lists and tables."""
    lines = md_text.strip().splitlines()
    html_output = []
    in_list = False
    in_table = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_output.append("</ul>")
                in_list = False
            continue
            
        # Headers
        if line.startswith("###"):
            if in_list: html_output.append("</ul>"); in_list = False
            html_output.append(f"<h4 style='color: var(--accent-blue); margin: 1.5rem 0 0.5rem;'>{line.strip('# ')}</h4>")
        
        # Lists
        elif line.startswith("*") or line.startswith("-"):
            if not in_list:
                html_output.append("<ul style='padding-left: 1.2rem; margin-bottom: 1rem; color: var(--text-secondary); line-height: 1.6;'>")
                in_list = True
            # Handle bolding in list items - more robust regex
            item = line.strip("* -")
            item = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color: #fff;'>\1</strong>", item)
            html_output.append(f"<li style='margin-bottom: 0.3rem;'>{item}</li>")
            
        # Tables
        elif "|" in line:
            if not in_table:
                html_output.append("<div style='overflow-x: auto; margin: 1rem 0;'><table style='width: 100%; border-collapse: collapse; font-size: 0.85rem; color: var(--text-secondary);'>")
                in_table = True
            
            if "---" in line: continue # Skip separator
            
            cells = [c.strip() for c in line.split("|") if c.strip() or line.count("|") > 1]
            if not cells: continue
            
            is_header = "打ち上げ日" in line # Heuristic for header
            tag = "th" if is_header else "td"
            style = "border: 1px solid rgba(255,255,255,0.1); padding: 0.6rem; text-align: left;"
            if is_header: style += " background: rgba(255,255,255,0.05); color: #fff;"
            
            row_html = "<tr>"
            for cell in cells:
                # Handle images/emojis and links
                cell = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2' target='_blank' style='color: var(--accent-blue); text-decoration: none;'>\1</a>", cell)
                cell = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", cell)
                row_html += f"<{tag} style='{style}'>{cell}</{tag}>"
            row_html += "</tr>"
            html_output.append(row_html)
            
        else:
            if in_list: html_output.append("</ul>"); in_list = False
            if in_table: html_output.append("</table></div>"); in_table = False
            html_output.append(f"<p style='margin-bottom: 1rem;'>{line}</p>")
            
    if in_list: html_output.append("</ul>")
    if in_table: html_output.append("</table></div>")
    
    return "\n".join(html_output)

def extract_data(log_path):
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading log: {e}")
        return None

    # Extract Ippo Index
    ippo_pattern = r"\u30e9\u30f3\u30af\s+([A-Z])\*\*\s+\((\d+)\s+/\s+100\)"
    ippo_match = re.search(ippo_pattern, content)
    index_rank = ippo_match.group(1) if ippo_match else "N/A"
    index_score = ippo_match.group(2) if ippo_match else "0"

    # Extract Rocket Intelligence Section
    # Find section starting with "宇宙ロケット打ち上げ最新情報"
    keyword = "\u5b87\u5b99\u30ed\u30b1\u30c3\u30c8\u6253\u3061\u4e0a\u3052\u6700\u65b0\u60c5\u5831"
    rocket_full_html = ""
    start_idx = content.find(keyword)
    if start_idx != -1:
        # Move back to find the "## " header
        header_start = content.rfind("##", 0, start_idx)
        if header_start != -1:
            # Find the end of section (next ## header or end)
            header_end = content.find("\n## ", start_idx)
            section_text = content[header_start:header_end].strip() if header_end != -1 else content[header_start:].strip()
            # Remove the header line
            section_text = re.sub(r"^##.*?\n", "", section_text)
            rocket_full_html = md_to_html(section_text)

    # Simplified Artemis II status for the card summary
    rocket_status = "No updates."
    artemis_match = re.search(r"Artemis II.*?\u6700\u65b0\u72b6\u6cc1[^\n]*?[:：]\s*([^\n\*]+)", content)
    if artemis_match:
        rocket_status = artemis_match.group(1).strip()
    
    return {
        "date": datetime.now().strftime("%Y.%m.%d"),
        "starry_sky": {
            "rank": index_rank,
            "score": int(index_score)
        },
        "rocket": {
            "mission": "Artemis II",
            "status": rocket_status,
            "full_html": rocket_full_html
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
