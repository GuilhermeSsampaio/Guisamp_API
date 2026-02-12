import re

def extract_title(content):
    match = re.search(r'#+\s+\*\*(.+?)\*\*', content)
    if match:
        return match.group(1).strip()
    match = re.search(r'#+\s+(.+)', content)
    if match:
        return match.group(1).strip()
    return None