#!/bin/bash

set -e

MOD_NAME="jira_mod"
TARGET_DIR="/c/Users/jiraa/Documents/Electronic Arts/The Sims 4/Mods"

echo "Compiling main.py..."
python -m py_compile main.py

echo "Moving .pyc file from __pycache__..."
PYC_FILE=$(ls __pycache__/main.*.pyc)
mv "$PYC_FILE" ./main.pyc

echo "Removing __pycache__ directory..."
rm -rf __pycache__

echo "Creating zip file..."
zip "$MOD_NAME.zip" main.py main.pyc

echo "Moving zip to Sims 4 Mods folder..."
mv "$MOD_NAME.zip" "$TARGET_DIR"

echo "Renaming zip to .ts4script..."
mv "$TARGET_DIR/$MOD_NAME.zip" "$TARGET_DIR/$MOD_NAME.ts4script"

echo "Done! Mod built successfully."