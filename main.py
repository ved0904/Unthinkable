# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database
import llm_service

# Initialize FastAPI app
app = FastAPI(title="AI Customer Support Bot API")

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    database.init_db()

# Pydantic model for the incoming request body
class ChatRequest(BaseModel):
    session_id: str
    query: str

# API endpoint for chat interactions
@app.post("/chat", summary="Handle a customer chat query")
def handle_chat(request: ChatRequest):
    """
    This endpoint manages a customer support interaction.
    - It retrieves the conversation history using the session_id.
    - It calls the LLM service to generate a response.
    - It saves the new interaction to the database.
    """
    try:
        # 1. Retrieve conversation history for context 
        print("--- SERVER HIT: A request was received by handle_chat ---")
        history = database.get_conversation(request.session_id)

        # 2. Generate a response from the LLM 
        response_text = llm_service.generate_response(
            query=request.query,
            history=history
        )

        # 3. Save the new exchange for session tracking [cite: 12]
        database.add_to_conversation(
            session_id=request.session_id,
            user_query=request.query,
            bot_response=response_text
        )

        return {"session_id": request.session_id, "response": response_text}

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root endpoint for health check")
def read_root():
    return {"message": "AI Customer Support Bot is running."}