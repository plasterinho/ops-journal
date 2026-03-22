import yaml

def parse_tasks(markdown_text):
    """Parses a markdown string to extract tasks and their associated checks.
    Args:
        markdown_text (str): The markdown string containing task definitions.
    Returns:
        list: A list of task dictionaries with 'text', 'claimed', and optional 'check' keys.
    """
    lines = markdown_text.splitlines()
    tasks = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("- ["):
            claimed = "[x]" in line
            text = line.split("]", 1)[1].strip()

            task = {
                "text": text,
                "claimed": claimed,
            }

            # Check for YAML block
            if i + 1 < len(lines) and "check:" in lines[i + 1]:
                j = i + 1
                check_lines = []

                while j < len(lines) and not lines[j].strip().startswith("  "):
                    check_lines.append(lines[j].strip())
                    j += 1
            
                check_yaml = "\n".join(check_lines)
                task["check"] = yaml.safe_load(check_yaml)["check"] if check_yaml else None

                i = j - 1

            tasks.append(task)

        i += 1

    return tasks