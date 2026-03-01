const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const CONTENT_DIR = path.join(__dirname, '../content/weeks');
const VALID_STATUSES = ['pending', 'done', 'verified'];

let hasError = false;

function validateFile(filePath) {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const { data, content } = matter(raw);

    const errors = [];

    // Frontmatter validation
    if (!data.id || !/^[a-z0-9-]+$/.test(data.id)) {
        errors.push('Missing or invalid "id" (must be lowercase letters, numbers, and hyphens only)');
    }

    if (!Number.isInteger(data.week) || data.week < 1) {
        errors.push('Missing or invalid "week" (must be a positive integer)');
    }

    if (!data.title || data.title.trim().length === 0) {
        errors.push('Missing or empty "title"');
    }

    if (!VALID_STATUSES.includes(data.status)) {
        errors.push(`Missing or invalid "status" (must be one of: ${VALID_STATUSES.join(', ')})`);
    }

    if (!data.created_at) {
        errors.push('Missing "created_at"');
    }

    // Body validation
    if (!content.includes('## Description')) {
        errors.push('Missing "## Description" section in the body');
    }

    if (!content.includes('## Evidence')) {
        errors.push('Missing "## Evidence" section in the body');
    } else {
        const evidenceSection = content.split('## Evidence')[1];
        if (!evidenceSection || !evidenceSection.includes("- ")) {
            errors.push('The "## Evidence" section must contain a list of evidence items (e.g., "- Evidence item")');
        }
    }

    if (errors.length > 0) {
        console.error(`Validation errors in file: ${filePath}`);
        errors.forEach(error => console.error(`  - ${error}`));
        hasError = true;
    }

    function walk(dir) {
        fs.readdirSync(dir).forEach(file => {
            const fullPath = path.join(dir, file);
            if (fs.statSync(fullPath).isDirectory()) {
                walk(fullPath);
            } else if (file.endsWith('.md')) {
                validateFile(fullPath);
            }
        });
    }

walk(CONTENT_DIR);

if (hasError) {
    console.error('Validation failed. Please fix the errors above.');
    process.exit(1);
} else {
    console.log('All files are valid!');
}