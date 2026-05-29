
import json
import re
import os
from openai import OpenAI


# =========================================================
# GROQ CLIENT
# =========================================================
api_key_groq = os.getenv("GROQ_API_KEY")
client = OpenAI(
    api_key=api_key_groq,
    base_url="https://api.groq.com/openai/v1"
)


# =========================================================
# SAFE NUMBER PARSER
# =========================================================

def to_number(val):

    if val is None:
        return 0

    try:

        cleaned = re.sub(
            r"[^0-9.-]",
            "",
            str(val).replace(",", "")
        )

        return float(cleaned)

    except:
        return 0


# =========================================================
# CLEAN JSON RESPONSE
# =========================================================

def clean_json(text):

    try:

        cleaned = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        first = cleaned.find("{")
        last = cleaned.rfind("}")

        if first != -1 and last != -1:

            cleaned = cleaned[first:last + 1]

        return json.loads(cleaned)

    except Exception:

        return {
            "success": False,
            "error": "Invalid JSON from AI",
            "raw": text
        }


# =========================================================
# AI CALL
# =========================================================

async def call_ai(prompt, retry=2):

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.1,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",

                    "content": """
You are a Tier-1 institutional forex trading AI.

You think like:
- hedge funds
- smart money
- macro desks
- banks
- liquidity operators

You NEVER behave like a retail trader.

You focus on:
- DXY
- macro economics
- bond yields
- liquidity
- institutional positioning
- support resistance
- volatility
- geopolitical risk

You generate:
- precise BUY zones
- precise SELL zones
- stop loss
- take profit
- institutional setups

RETURN STRICT VALID JSON ONLY.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as err:

        if retry > 0:
            return await call_ai(prompt, retry - 1)

        raise err


# =========================================================
# MAIN FOREX AI ENGINE
# =========================================================

async def get_forex_ai_result(

    technical_data,
    news_data,
    signal_data
):

    try:

        # =========================================================
        # SAFE DATA BUILD
        # =========================================================

        raw_data = {

            "signal": {

                "symbol":
                    signal_data.get("symbol"),

                "direction":
                    signal_data.get("direction"),

                "entry_price":
                    to_number(
                        signal_data.get("entry_price")
                    ),

                "target_price":
                    to_number(
                        signal_data.get("target_price")
                    ),

                "stop_loss":
                    to_number(
                        signal_data.get("stop_loss")
                    ),

                "current_price":
                    to_number(
                        signal_data.get("current_price")
                    ),

                "status":
                    signal_data.get("status"),

                "roi":
                    to_number(
                        signal_data.get("roi")
                    )
            },

            "technicals":
                technical_data,

            "news":
                news_data
        }

        # =========================================================
        # PROMPT
        # =========================================================

        prompt = f"""
You are a Tier-1 institutional forex AI.

Analyze the forex market like:
- banks
- hedge funds
- smart money
- liquidity traders
- macro desks

==================================================
ANALYZE
==================================================

1. Market structure
2. Trend direction
3. RSI
4. MACD
5. EMA/SMA alignment
6. ADX trend strength
7. Volatility
8. Institutional positioning
9. Macro sentiment
10. Geopolitical risk
11. DXY impact

==================================================
IMPORTANT RULES
==================================================

1. IF:
- trend bearish
- MACD bearish
- momentum weak

THEN:
market bias should support SELL.

2. IF:
- trend bullish
- MACD bullish

THEN:
market bias should support BUY.

3. IF:
- ADX below 20

THEN:
market is weak trend or range bound.

4. IF:
- geopolitical tension high
- oil prices rising

THEN:
USD likely stronger.

==================================================
ENTRY + TP + SL RULES
==================================================

1. IF marketBias = SELL:
- create realistic SELL zone
- stop loss ABOVE resistance
- take profit near support

2. IF marketBias = BUY:
- create realistic BUY zone
- stop loss BELOW support
- take profit near resistance

3. Use:
- ATR
- support
- resistance
- volatility
- current price

to calculate:
- entry
- stop loss
- take profits

4. Minimum risk reward:
1:1.5 or higher

==================================================
RETURN STRICT JSON
==================================================

{{
    "pair": "",

    "marketBias": "",

    "trendStrength": "",

    "volatility": "",

    "momentum": "",

    "macroSentiment": "",

    "liquidityCondition": "",

    "institutionalView": "",

    "tradeQuality": "",

    "probabilityScore": 0,

    "riskLevel": "",

    "signalValidation": "",

    "bestAction": "",

    "entryZone": "",

    "buyZone": "",

    "sellZone": "",

    "takeProfit1": "",

    "takeProfit2": "",

    "stopLoss": "",

    "riskRewardRatio": "",

    "summary": "",

    "warnings": []
}}

==================================================
MARKET DATA
==================================================

{json.dumps(raw_data, indent=2)}

==================================================
IMPORTANT
==================================================

RETURN ONLY VALID JSON.
NO MARKDOWN.
NO EXTRA TEXT.
"""

        # =========================================================
        # AI CALL
        # =========================================================

        raw = await call_ai(prompt)

        # =========================================================
        # CLEAN RESPONSE
        # =========================================================

        result = clean_json(raw)

        return result

    except Exception as error:

        return {

            "success": False,

            "error": str(error)
        }

