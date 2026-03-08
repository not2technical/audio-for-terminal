#!/bin/bash

# VoxTerm Rebrand Verification Script
# This script verifies that all branding changes were applied correctly

echo "======================================================"
echo "🔍 VoxTerm Rebrand Verification"
echo "======================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

PASSED=0
FAILED=0

# Function to check if string exists in file
check_contains() {
    local file="$1"
    local search="$2"
    local description="$3"

    if grep -q "$search" "$file" 2>/dev/null; then
        echo "✅ $description"
        ((PASSED++))
        return 0
    else
        echo "❌ $description"
        ((FAILED++))
        return 1
    fi
}

# Function to check if OLD string does NOT exist in file
check_not_contains() {
    local file="$1"
    local search="$2"
    local description="$3"

    if ! grep -q "$search" "$file" 2>/dev/null; then
        echo "✅ $description"
        ((PASSED++))
        return 0
    else
        echo "❌ $description (old branding still present)"
        ((FAILED++))
        return 1
    fi
}

echo "📋 Checking Documentation Files..."
echo ""

check_contains "README.md" "# 🎤 VoxTerm" "README.md: VoxTerm title"
check_contains "README.md" "Why VoxTerm?" "README.md: Why VoxTerm section"
check_contains "README.md" "VoxTerm vs Alternatives" "README.md: Comparison table"
check_contains "README.md" "https://github.com/not2technical/voxterm" "README.md: Repository URL"
check_not_contains "README.md" "Audio for Terminal" "README.md: No old name"

echo ""
check_contains "QUICKSTART.md" "VoxTerm" "QUICKSTART.md: VoxTerm branding"
check_contains "QUICKSTART.md" "cd voxterm" "QUICKSTART.md: Updated paths"

echo ""
check_contains "CHEATSHEET.md" "VoxTerm" "CHEATSHEET.md: VoxTerm branding"

echo ""
check_contains "STREAMING_GUIDE.md" "VoxTerm" "STREAMING_GUIDE.md: VoxTerm branding"

echo ""
check_contains "LAUNCHER_GUIDE.md" "VoxTerm" "LAUNCHER_GUIDE.md: VoxTerm branding"

echo ""
echo "📋 Checking Python Code..."
echo ""

check_contains "main_streaming.py" "VoxTerm" "main_streaming.py: VoxTerm branding"
check_not_contains "main_streaming.py" "Voice Dictation for Terminal" "main_streaming.py: No old name"

echo ""
echo "📋 Checking Shell Scripts..."
echo ""

check_contains "create-app.sh" 'APP_NAME="VoxTerm"' "create-app.sh: App name"
check_contains "create-app.sh" "com.voxterm.app" "create-app.sh: Bundle identifier"
check_not_contains "create-app.sh" "VoiceDictation" "create-app.sh: No old app name"

echo ""
check_contains "setup.sh" "VoxTerm" "setup.sh: VoxTerm branding"

echo ""
check_contains "toggle-streaming.sh" "VoxTerm" "toggle-streaming.sh: VoxTerm branding"

echo ""
check_contains "run-streaming.sh" "VoxTerm" "run-streaming.sh: VoxTerm branding"

echo ""
echo "======================================================"
echo "📊 Verification Results"
echo "======================================================"
echo ""
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All checks passed! Rebrand is complete."
    echo ""
    echo "📝 Next Steps:"
    echo "   1. Rename GitHub repository: audio-for-terminal → voxterm"
    echo "   2. Update local remote:"
    echo "      git remote set-url origin https://github.com/not2technical/voxterm.git"
    echo "   3. Rename local directory:"
    echo "      cd ~ && mv audio-for-terminal voxterm"
    echo "   4. Test functionality:"
    echo "      cd ~/voxterm && ./toggle.sh"
    echo "   5. Commit and push changes"
    echo ""
    exit 0
else
    echo "⚠️  Some checks failed. Review the output above."
    echo ""
    exit 1
fi
