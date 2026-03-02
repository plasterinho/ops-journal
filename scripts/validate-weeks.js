const fs = require("fs");
const path = require("path");

const CONTENT_DIR = path.join(__dirname, "../docs/journal");

let hasError = false;
let totalFiles = 0;
let failedFiles = 0;

function validateFile(filePath) {
  totalFiles++;

  const relativePath = path.relative(process.cwd(), filePath);
  const content = fs.readFileSync(filePath, "utf-8");
  const errors = [];

  const lines = content.split("\n").map(l => l.trim());
  const firstNonEmpty = lines.find(l => l.length > 0);

  // --- Title validation ---
  if (!firstNonEmpty || !firstNonEmpty.startsWith("# Week")) {
    errors.push("Missing or invalid top-level '# Week' title");
  }

  // --- Required sections ---
  const goalIndex = content.indexOf("## Goal");
  const evidenceIndex = content.indexOf("## Evidence");

  if (goalIndex === -1) {
    errors.push("Missing '## Goal' section");
  }

  if (evidenceIndex === -1) {
    errors.push("Missing '## Evidence' section");
  } else {
    const evidenceSection = content.split("## Evidence")[1];
    if (!evidenceSection || !evidenceSection.includes("- ")) {
      errors.push("Evidence section must contain at least one bullet");
    }
  }

  // --- Section order enforcement ---
  if (goalIndex !== -1 && evidenceIndex !== -1) {
    if (goalIndex > evidenceIndex) {
      errors.push("'## Goal' must appear before '## Evidence'");
    }
  }

  // --- Filename ↔ Title consistency ---
  const match = filePath.match(/week-(\d+)\.md$/);
  const titleMatch = firstNonEmpty
    ? firstNonEmpty.match(/^# Week (\d+)/)
    : null;

  if (!match) {
    errors.push("Filename does not match week-XX.md pattern");
  } else if (!titleMatch) {
    errors.push("Title does not match '# Week <number>' format");
  } else {
    const fileWeek = parseInt(match[1], 10);
    const titleWeek = parseInt(titleMatch[1], 10);

    if (fileWeek !== titleWeek) {
      errors.push(
        `Filename week number (${fileWeek}) does not match title week number (${titleWeek})`
      );
    }
  }

  // --- Output errors ---
  if (errors.length > 0) {
    failedFiles++;
    console.error(`\n❌ ${relativePath}`);
    errors.forEach(e => console.error("   - " + e));
    hasError = true;
  }
}

// --- Iterate files ---
fs.readdirSync(CONTENT_DIR)
  .filter(f => f.endsWith(".md"))
  .forEach(f => validateFile(path.join(CONTENT_DIR, f)));

// --- Final summary ---
if (hasError) {
  console.error(`\n${failedFiles}/${totalFiles} week documents failed validation.`);
  process.exit(1);
} else {
  console.log(`All ${totalFiles} week documents valid.`);
}