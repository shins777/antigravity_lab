#!/usr/bin/env bash
# Script triggered by Antigravity CLI PostToolUse hook on file edit/creation tools.

# Read JSON payload from stdin
PAYLOAD=$(cat)

# Extract tool call target file path (TargetFile for replace_file_content/write_to_file)
TARGET_FILE=$(echo "$PAYLOAD" | grep -o '"TargetFile":"[^"]*"' | head -n 1 | cut -d'"' -f4)

if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
    # Check if target file is a Python file (.py)
    if [[ "$TARGET_FILE" == *.py ]]; then
        # Run ruff/black formatting or autopep8/flake8 if available
        if command -v ruff &> /dev/null; then
            ruff format "$TARGET_FILE" &> /dev/null
            ruff check --fix "$TARGET_FILE" &> /dev/null
        elif command -v black &> /dev/null; then
            black "$TARGET_FILE" &> /dev/null
        fi

        # Run ESLint/Prettier if pre-configured for Python/polyglot files
        if command -v npx &> /dev/null; then
            npx prettier --write "$TARGET_FILE" &> /dev/null
            npx eslint --fix "$TARGET_FILE" &> /dev/null
        fi
    # If target file is a JavaScript/TypeScript/JSON/Markdown file
    elif [[ "$TARGET_FILE" =~ \.(js|jsx|ts|tsx|json|md)$ ]]; then
        if command -v npx &> /dev/null; then
            npx prettier --write "$TARGET_FILE" &> /dev/null
            npx eslint --fix "$TARGET_FILE" &> /dev/null
        fi
    fi
fi

# Always return empty valid JSON object required by PostToolUse contract
echo "{}"
