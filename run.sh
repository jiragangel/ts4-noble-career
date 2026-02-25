#!/bin/bash

# Configuration
MOD_NAME="jira_mod"
TARGET_DIR="/c/Users/jiraa/Documents/Electronic Arts/The Sims 4/Mods"

# 1. Filter and iterate through .py files
FILES=$(ls *.py 2>/dev/null)

if [ -z "$FILES" ]; then
    echo "No .py files found."
    exit 1
fi

echo "Compiling files..."
for FILE in $FILES; do
    python3 -m py_compile "$FILE"
    echo "Processed: $FILE"
done

# 2. Extract .pyc files and Rename them (Removing .cpython-314)
echo "Cleaning up filenames..."
find . -name "*.pyc" -exec mv {} . \;

for f in *.cpython-*.pyc; do
    [ -e "$f" ] || continue
    # This regex removes the .cpython-XX part (e.g., .cpython-314)
    NEW_NAME=$(echo "$f" | sed 's/\.cpython-[0-9]\{2,3\}//')
    mv "$f" "$NEW_NAME"
done

# 3. Zip all .pyc files into the mod package
# We use -m to "move" them into the zip (cleans up the loose .pyc files)
zip "$MOD_NAME.zip" *.py*

echo "---"
echo "Moving to Sims 4 Mods folder..."

# Ensure target directory exists (optional safety check)
mkdir -p "$TARGET_DIR"

# Move and rename to .ts4script in one go
mv "$MOD_NAME.zip" "$TARGET_DIR/$MOD_NAME.ts4script"

echo "Done! Mod built successfully at: $TARGET_DIR/$MOD_NAME.ts4script"

find . -name "*.pyc" -delete