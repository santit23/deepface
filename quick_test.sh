#!/bin/bash

# quick_test.sh - Quick test for feature/demographics-action branch

echo "Quick Test - feature/demographics-action branch"
echo "======================================"

# Check branch
current_branch=$(git branch --show-current 2>/dev/null || echo "")
if [ "$current_branch" != "feature/demographics-action" ]; then
    echo "Please run: git checkout feature/demographics-action"
    exit 1
fi

# Create test image if examples folder is empty
if [ ! -d "examples" ] || [ -z "$(ls -A examples 2>/dev/null)" ]; then
    echo "Creating test image..."
    mkdir -p examples
    python3 -c "
import numpy as np
import cv2
img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
cv2.imwrite('examples/test_image.jpg', img)
print('Created examples/test_image.jpg')
    "
fi

# Run test
echo "Running test analysis..."
./run_demo.sh single examples/test_image.jpg --detector opencv --output test_output

echo "======================================"
echo "Quick test completed! Check test_output/ folder"