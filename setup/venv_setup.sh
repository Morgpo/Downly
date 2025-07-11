#!/bin/bash
cd ..

echo "Setting up virtual environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
pip install -r setup/requirements.txt
deactivate

echo "Virtual environment setup complete."
