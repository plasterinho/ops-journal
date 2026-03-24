def enrich_markdown(tasks):
    """ Enrich markdown tasks with verification results. 
    This is a higher-level function that combines parsing and evaluation."""
    lines = []

    for t in tasks:
        lines.append(f"- [{'x' if t.get('claimed') else ' '}] {t['text']}")

        if t.get("verification"):
            status = t["verification"]["status"]
            msg = t["verification"]["message"]

            icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            lines.append(f"  - {icon} {status}: {msg}")

    return "\n".join(lines)