#!/bin/bash

# Ensure the script exits on any error
set -e

# Install dependencies
echo "Installing dependencies from requirements_diffusion.txt"
pip install -r requirements_diffusion.txt

echo "Installing dependencies from requirements_LLM.txt"
pip install -r requirements_LLM.txt

# Instructions for running the project
echo ""
echo "### How to run"
echo ""
echo "Navigate to the correct directory:"
echo ""
echo "    cd agentapi"
echo ""
echo "Then, run the FastAPI server:"
echo ""
echo "    uvicorn app.main:app --reload"
echo ""
echo "Finally, run the Streamlit client:"
echo ""
echo "    streamlit run client.py"
echo ""
