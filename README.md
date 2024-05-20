# Testing RAG using Alice's Adventures in Wonderland as data


## GCSP e Holanda

Research intended for my International GCSP program research, where I will delve into the Netherlands - where I will spend a semester studying artificial intelligence (grad - exchange program).

## Installation 


### Create virtual ambient in python (only first time)

    python -m venv venv

### Activate the venv

    venv\Scripts\activate

### Install the requirements

    pip install -r requirements-diffusiin.txt
    
    pip install -r requirements-LLM.txt

### How to run

Cd the correct directiory:

    cd agentapi

Then, run the FastAPI server:

    uvicorn app:app --reload

Finally, run the Streamlit client:

    streamlit run client.py
