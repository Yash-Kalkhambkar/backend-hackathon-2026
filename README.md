# Escalation Detector

An AI-powered FastAPI application that analyzes support conversations and determines if they need escalation to a human agent using Groq's LLM.

## What It Does

This application accepts multi-turn support conversations, uses an LLM (llama-3.1-8b-instant via Groq) to decide if escalation is needed, stores all decisions in a PostgreSQL database, and provides a clean web interface to submit conversations and view escalation history.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file should already contain:
```
DATABASE_URL=postgresql+psycopg2://[your-db-credentials]
GROQ_API_KEY=[your-groq-api-key]
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Open the Frontend

Open `frontend/index.html` in your browser, or serve it with:
```bash
python -m http.server 8080 --directory frontend
```

Then visit `http://localhost:8080`

## API Endpoints

### POST /escalation/check
Check if a conversation needs escalation.

```bash
curl -X POST http://localhost:8000/escalation/check \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TICKET-001",
    "conversation": "Customer: My account is locked and I need access NOW!\nAgent: Let me check that for you.\nCustomer: This is unacceptable! I have been waiting for 2 hours!"
  }'
```

Response:
```json
{
  "ticket_id": "TICKET-001",
  "escalate": true,
  "reason": "Customer is frustrated and demanding immediate action",
  "log_id": 1
}
```

### GET /escalation/logs
Retrieve all escalation logs (most recent first).

```bash
curl http://localhost:8000/escalation/logs
```

### GET /escalation/logs/{ticket_id}
Get all logs for a specific ticket.

```bash
curl http://localhost:8000/escalation/logs/TICKET-001
```

### GET /escalation/stats
Get escalation statistics.

```bash
curl http://localhost:8000/escalation/stats
```

Response:
```json
{
  "total": 50,
  "escalated": 12,
  "not_escalated": 38,
  "escalation_rate": 24.0
}
```

### GET /escalation/health
Health check endpoint.

```bash
curl http://localhost:8000/escalation/health
```

Response:
```json
{
  "status": "ok",
  "db": "connected",
  "llm": "configured"
}
```

## Using the Frontend

1. Open `frontend/index.html` in your browser
2. Enter a ticket ID (e.g., "TICKET-001")
3. Paste the support conversation in the textarea
4. Click "Check Escalation"
5. View the result with a color-coded badge (red for escalate, green for no escalation)
6. See recent logs in the table below

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Tech Stack

- FastAPI (sync endpoints)
- SQLAlchemy with psycopg2-binary
- PostgreSQL (cloud database)
- Groq Python SDK (llama-3.1-8b-instant)
- Pydantic Settings for configuration
- Vanilla HTML/CSS/JavaScript frontend
