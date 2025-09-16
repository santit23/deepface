#!/bin/bash

# Clone your repository
git clone https://github.com/your-username/deepface.git
cd deepface

# Install requirements
pip install -r requirements.txt

# Install additional dependencies
pip install opencv-python matplotlib

# Install the package in development mode
pip install -e .

echo "Installation complete!"