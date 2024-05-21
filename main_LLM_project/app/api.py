from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import get_agent_executor

class PromptRequest(BaseModel):
    prompt: str

def create_endpoint(agent_executors, character: str):
    async def endpoint(request: PromptRequest):
        return agent_executors[character].invoke({"input": request.prompt})
    return endpoint

def create_app(agent_executors):
    app = FastAPI(
        title="Alice's Wonderland Characters",
        version="1.0",
        description="An API to interact with Alice's Wonderland characters"
    )

    app.post("/alice")(create_endpoint(agent_executors, "Alice"))
    app.post("/white-rabbit")(create_endpoint(agent_executors, "White Rabbit"))
    app.post("/mad-hatter")(create_endpoint(agent_executors, "Mad Hatter"))
    app.post("/cheshire-cat")(create_endpoint(agent_executors, "Cheshire Cat"))
    app.post("/queen-of-hearts")(create_endpoint(agent_executors, "Queen of Hearts"))

    return app