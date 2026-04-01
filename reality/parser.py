import yaml
import re

# Regular expression to extract task IDs from HTML comments
ID_PATTERN = re.compile(r'<!--\s*id:\s*(.*?)\s*-->')

def extract_id(line):
    """Extracts a task ID from an HTML comment in the line, if present."""
    match = ID_PATTERN.search(line)
    return match.group(1) if match else None

def parse_tasks(markdown_text):
    """Extract tasks from markdown.
    """
    lines = markdown_text.splitlines()
    tasks = []

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        if not line.startswith("- ["):
            i += 1
            continue
        
        claimed = "[x]" in line
        text = line.split("]", 1)[1].strip()
        task_id = extract_id(raw_line)

        tasks.append({
            "text": text,
            "claimed": claimed,
            "id": task_id,
        })

        i += 1

    return tasks