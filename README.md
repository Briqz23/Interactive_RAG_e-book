# Testing RAG using Alice's Adventures in Wonderland as data

[![Demo]](https://youtu.be/fdQ2I20hkBU)


## GCSP e Holanda

Research intended for my International GCSP program research, where I will delve into the Netherlands - where I will spend a semester studying artificial intelligence (grad - exchange program).

## Installation 


### Create virtual ambient in python (only first time)

    python -m venv venv

### Activate the venv

    venv\Scripts\activate

### Install the requirements

    pip install -r requirements_diffusion.txt
    
    pip install -r requirements_LLM.txt

### How to run

Cd the correct directiory:

    cd agentapi

Then, run the FastAPI server:

    uvicorn app:app --reload

Finally, run the Streamlit client:

    streamlit run client.py
