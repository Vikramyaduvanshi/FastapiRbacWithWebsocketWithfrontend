
import json
from openai import OpenAI
import os

api_key_groq = os.getenv("GROQ_API_KEY")
client = OpenAI(
    api_key=api_key_groq,
    base_url="https://api.groq.com/openai/v1"
)


def clean_json(text):

    try:

        cleaned = ( text .replace("```json", "") .replace("```", "") .strip())

        first = cleaned.find("{")
        last = cleaned.rfind("}")

        if first != -1 and last != -1:
            cleaned = cleaned[first:last + 1]

        return json.loads(cleaned)

    except Exception:

        return {
            "success": False,
            "error": "Invalid JSON",
            "raw": text
        }


async def extract_forex_intent(user_text):

    prompt = f"""
You are an institutional forex assistant.

Extract trading intent from user text.

RULES:

1. RETURN STRICT JSON ONLY
2. NEVER ADD EXTRA TEXT
3. Detect:
   - action
   - forex pair
   - direction
   - purpose

4. Normalize symbols:
   eur/usd -> EURUSD
   gbp jpy -> GBPJPY
   xauusd -> XAUUSD

5. If direction missing:
   return null

6. If pair missing:
   return null

================================================

RETURN FORMAT:

{{
    "action": "",
    "symbol": "",
    "direction": "",
    "purpose": ""
}}

================================================

USER TEXT:
{user_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        response_format={
            "type": "json_object"
        },

        messages=[

            {
                "role": "system",
                "content": (
                    "You extract forex trading intent."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw = response.choices[0].message.content

    return clean_json(raw)


