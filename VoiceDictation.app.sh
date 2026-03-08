#!/bin/bash

# VoxTerm Quick Launcher
# Double-click this to start VoxTerm

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Open a new Terminal window and run the app
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$DIR' && source venv/bin/activate && python main.py; exit"
end tell
EOF
