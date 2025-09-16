#!/bin/bash

# Bash script to run DeepFace analysis

# Set default image path
IMAGE_PATH="examples/person.jpg"

echo "Select an option:"
echo "1) Single image analysis (default settings)"
echo "2) Single image analysis (custom output directory)"
echo "3) Single image analysis (specific detector)"
echo "4) Batch image analysis"

read -p "Enter option number (1-4): " OPTION

case $OPTION in
    1)
        echo "Running single image analysis with default settings..."
        python3 run_analysis.py --image "$IMAGE_PATH"
        ;;
    2)
        read -p "Enter output directory name: " OUTPUT_DIR
        echo "Running single image analysis with custom output directory '$OUTPUT_DIR'..."
        python3 run_analysis.py --image "$IMAGE_PATH" --output "$OUTPUT_DIR"
        ;;
    3)
        read -p "Enter detector to use (e.g., mtcnn, ssd, dlib, retinaface): " DETECTOR
        read -p "Enter output directory name: " OUTPUT_DIR
        echo "Running single image analysis with detector '$DETECTOR' and output '$OUTPUT_DIR'..."
        python3 run_analysis.py --image "$IMAGE_PATH" --detector "$DETECTOR" --output "$OUTPUT_DIR"
        ;;
    4)
        echo "Running batch image analysis..."
        python3 enhanced_deepface_analysis.py
        ;;
    *)
        echo "Invalid option. Exiting."
        ;;
esac
