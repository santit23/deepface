#!/bin/bash

# setup.sh - Setup for feature/demographics-action branch

set -e

echo "Setting up Enhanced DeepFace Demographic Analysis"
echo "Branch: feature/demographics-action"
echo "======================================"

# Check if we're in the right branch
current_branch=$(git branch --show-current 2>/dev/null || echo "")
if [ "$current_branch" != "feature/demographics-action" ]; then
    echo "Switching to feature/demographics-action branch..."
    git checkout feature/demographics-action
    if [ $? -ne 0 ]; then
        echo "Error: Could not switch to feature/demographics-action branch"
        echo "Make sure the branch exists: git branch -a"
        exit 1
    fi
fi

echo "✅ On branch: feature/demographics-action"

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt


# Make scripts executable
chmod +x run_demo.sh

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add images to examples/ folder:"
echo "   mkdir -p examples"
echo "   # Add your jpg/png images to examples/"
echo ""
echo "2. Run analysis:"
echo "   ./run_demo.sh single examples/your_image.jpg"
echo "   ./run_demo.sh batch examples/"
echo ""
echo "3. Or use direct Python commands:"
echo "   python run_analysis.py --image examples/photo.jpg"
echo "   python enhanced_deepface_analysis.py examples/"