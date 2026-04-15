# LLM service for escalation detection using Groq API
import json
from groq import Groq
from app.config import settings

# Initialize Groq client with API key
client = Groq(api_key=settings.GROQ_API_KEY)


def check_escalation(conversation: str) -> dict:
    """
    Call Groq LLM to determine if a support conversation needs escalation.
    Returns a dict with 'escalate' (bool) and 'reason' (str).
    Falls back to safe default if LLM call or JSON parsing fails.
    """
    try:
        # Build the prompt for the LLM
        system_message = "You are a support escalation expert."
        user_message = f"""Read this support conversation and decide if it needs escalation to a human agent.
Reply as JSON only, no extra text:
{{"escalate": true or false, "reason": "one line explanation"}}

Conversation:
{conversation}"""
        
        # Call Groq API with llama-3.1-8b-instant model
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=200
        )
        
        # Extract response content
        content = chat_completion.choices[0].message.content.strip()
        print(f"LLM raw response: {content}")
        
        # Parse JSON response
        result = json.loads(content)
        
        # Validate response structure
        if "escalate" not in result or "reason" not in result:
            raise ValueError("Missing required fields in LLM response")
        
        return {
            "escalate": bool(result["escalate"]),
            "reason": str(result["reason"])
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return {
            "escalate": False,
            "reason": "Unable to parse LLM response"
        }
    except Exception as e:
        print(f"LLM service error: {e}")
        return {
            "escalate": False,
            "reason": f"LLM service error: {str(e)}"
        }
