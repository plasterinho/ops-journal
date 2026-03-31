import yaml

def parse_tasks(markdown_text):
    lines = markdown_text.splitlines()
    tasks = []

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        if line.startswith("- ["):
            claimed = "[x]" in line
            text = line.split("]", 1)[1].strip()

            task = {
                "text": text,
                "claimed": claimed,
            }

            # Detect check block
            if i + 1 < len(lines) and lines[i + 1].startswith("  check:"):
                j = i + 1
                check_lines = []

                # base indentation (2 spaces before 'check:')
                base_indent = len(lines[j]) - len(lines[j].lstrip())

                while j < len(lines):
                    current_line = lines[j]

                    # stop if new task
                    if current_line.strip().startswith("- ["):
                        break

                    # stop if dedented (but allow first line)
                    current_indent = len(current_line) - len(current_line.lstrip())
                    if j > i + 1 and current_indent <= base_indent:
                        break

                    check_lines.append(current_line.strip())
                    j += 1

                check_yaml = "\n".join(check_lines)

                parsed = yaml.safe_load(check_yaml)
                task["check"] = parsed.get("check") if parsed else None

                i = j - 1

            tasks.append(task)

        i += 1

    return tasks