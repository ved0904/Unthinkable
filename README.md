# AI Customer Support Bot

An AI-powered customer support bot that answers questions based on a provided FAQ dataset and intelligently escalates complex queries to human agents.

## 🎯 Features

- **FAQ-based responses**: Answers customer queries using predefined FAQs
- **Conversation memory**: Tracks entire conversation history per session
- **Smart escalation**: Automatically escalates queries that can't be answered from FAQs
- **RESTful API**: Easy-to-integrate FastAPI backend
- **Session management**: SQLite database for persistent conversation tracking

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **LLM Integration**: Google Gemini 2.5 Flash
- **API Framework**: FastAPI with Pydantic validation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-customer-support-bot.git
cd ai-customer-support-bot
```

### 2. Create and activate a virtual environment

**Windows (Git Bash/MINGW64):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your actual API key:

```
LLM_API_KEY="your_actual_gemini_api_key_here"
```

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

## 📡 API Usage

### Health Check
```bash
curl http://127.0.0.1:8000/
```

### Chat Endpoint

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "user123", "query": "What are your shipping options?"}'
```

**Response:**
```json
{
  "session_id": "user123",
  "response": "We offer standard shipping (5-7 business days) and express shipping (1-3 business days)."
}
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧪 Testing

Run the test script to verify your setup:

```bash
python test.py
```

This will:
- Check if your API key is loaded correctly
- List available Gemini models
- Test API connectivity

## 📁 Project Structure

```
ai-customer-support-bot/
├── main.py              # FastAPI application and endpoints
├── database.py          # Database models and session management
├── llm_service.py       # LLM integration and prompt engineering
├── faqs.txt            # FAQ knowledge base
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── test.py            # API testing script
```

## 🤖 How It Works

1. **User sends a query** via POST request to `/chat` endpoint
2. **System retrieves conversation history** from SQLite database using session_id
3. **LLM analyzes the query** along with conversation context and FAQs
4. **Response generation**:
   - If answer is in FAQs → Direct answer provided
   - If query is ambiguous → Asks for clarification
   - If cannot answer → Escalates with "ESCALATE:" prefix
5. **Conversation saved** to database for future context

## 🎯 Core LLM Prompt

The bot's behavior is guided by this system prompt:

```
You are an AI customer support assistant. Your goal is to help users 
by answering their questions based on the provided FAQs.

Instructions:
1. Analyze the user's query and the conversation history.
2. If the query can be answered using the FAQs, provide the answer directly.
3. If the query is ambiguous, ask for clarification.
4. Escalation Rule: If you cannot answer the question using the FAQs, 
   you MUST respond with the exact phrase "ESCALATE: " followed by a 
   summary of the conversation and a suggested next action for the human agent.
```

## 📝 Customizing FAQs

Edit `faqs.txt` to add or modify FAQs:

```
Q: Your question here?
A: Your answer here.

Q: Another question?
A: Another answer.
```

The bot will automatically use the updated FAQs without code changes.

## 🔧 Configuration

### Using a different LLM model

Edit `llm_service.py` line 11:

```python
# Change from gemini-2.5-flash to another model
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={LLM_API_KEY}"
```

Available models:
- `gemini-2.5-flash` - Fast and efficient (default)
- `gemini-2.5-pro` - Most capable
- `gemini-flash-latest` - Always uses latest stable version

## 🚨 Troubleshooting

### "Error: Could not connect to the LLM service"

1. Check if your API key is correct in `.env`
2. Verify Generative Language API is enabled: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
3. Ensure you're using a valid model name
4. Check your internet connection

### Database errors

Delete the database file and restart:
```bash
rm support_bot.db
python -m uvicorn main:app --reload
```

### Import errors

Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

Your Name - [GitHub Profile](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- FastAPI for the excellent web framework
- SQLAlchemy for database ORM