import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
LLM_API_KEY = os.getenv("LLM_API_KEY")
# Using Google Gemini API
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={LLM_API_KEY}"

# --- Load FAQs ---
with open("faqs.txt", "r") as f:
    faqs = f.read()

def generate_response(query: str, history: list) -> str:
    """
    Generates a response using the LLM, conversation history, and FAQs.
    Handles escalation logic.
    """
    if not LLM_API_KEY:
        return "Error: LLM_API_KEY not configured."

   
    system_prompt = f"""
    You are an AI customer support assistant. Your goal is to help users by answering their questions based on the provided FAQs.

    **FAQs:**
    {faqs}

    **Instructions:**
    1. Analyze the user's query and the conversation history.
    2. If the query can be answered using the FAQs, provide the answer directly.
    3. If the query is ambiguous, ask for clarification.
    4. **Escalation Rule**: If you cannot answer the question using the FAQs, you MUST respond with the exact phrase "ESCALATE: " followed by a summary of the conversation and a suggested next action for the human agent.
    """

   
    formatted_history = "\n".join([f"User: {h.user_query}\nAI: {h.bot_response}" for h in history])

    # Construct the final prompt for the LLM
    final_prompt = f"{system_prompt}\n\n--- Conversation History ---\n{formatted_history}\n\n--- Current Query ---\nUser: {query}\nAI:"

    # --- LLM API Call (Example for Google Gemini) ---
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": final_prompt}]
        }]
    }

    print("--- DEBUG INFO ---")
    print(f"API Key Present: {bool(LLM_API_KEY)}")
    print(f"API Key Length: {len(LLM_API_KEY) if LLM_API_KEY else 0}")
    print(f"API URL: {GEMINI_API_URL[:80]}...")  # Don't print full URL with key
    print("--- END DEBUG INFO ---")
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
        
        # Print detailed error info
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text[:500]}")  # First 500 chars
        
        response.raise_for_status()
        
        data = response.json()
        # The path to the text might differ for other LLMs
        return data['candidates'][0]['content']['parts'][0]['text'].strip()

    except requests.exceptions.Timeout:
        print("API Request Timeout")
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
        return "Error: Could not connect to the LLM service. Check your API key and network connection."
    except (KeyError, IndexError) as e:
        print(f"API Response Error: {e} - Response: {response.text}")
        return "Error: Invalid response format from the LLM."