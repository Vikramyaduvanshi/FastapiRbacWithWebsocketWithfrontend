
import asyncio
import httpx


GNEWS_API_KEY = "d79b544b4e9bec9b8e616fefa95042bf"


queries = [

    # FOREX + MAJOR CURRENCIES
    "forex OR USD OR EUR OR GBP OR JPY OR CHF OR AUD OR CAD OR NZD OR INR OR CNY",

    # CENTRAL BANKS
    "Fed OR FOMC OR ECB OR BOJ OR BOE OR RBA OR BOC OR RBI OR SNB OR PBOC OR RBNZ",

    # MACRO ECONOMICS
    '"interest rates" OR inflation OR CPI OR PPI OR NFP OR payrolls OR unemployment OR GDP OR recession',

    # BONDS + DXY
    'DXY OR "bond yields" OR "treasury yields"',

    # COMMODITIES
    "gold OR XAU OR silver OR oil OR crude OR brent OR WTI OR OPEC",

    # GEOPOLITICS
    "war OR sanctions OR tariffs OR geopolitics OR Iran OR Israel OR Russia OR Ukraine OR China OR Taiwan",

    # RISK SENTIMENT
    '"risk-on" OR "risk-off"',
]


async def fetch_all_news():

    all_articles = []

    try:

        async with httpx.AsyncClient(timeout=20) as client:

            for q in queries:

                try:

                    response = await client.get(
                        "https://gnews.io/api/v4/search",
                        params={
                            "q": q,
                            "lang": "en",
                            "max": 5,
                            "sortby": "publishedAt",
                            "token": GNEWS_API_KEY,
                        },
                    )

                    data = response.json()

                    if data.get("articles"):

                        all_articles.extend(
                            data["articles"]
                        )

                    # DELAY
                    await asyncio.sleep(1.5)

                except Exception as err:

                    print(f"❌ Failed Query: {q}")
                    print(err)

        # =========================
        # REMOVE DUPLICATES
        # =========================

        unique = []

        titles = set()

        for article in all_articles:

            title = article.get("title")

            if title not in titles:

                titles.add(title)

                unique.append(article)

        # =========================
        # SORT LATEST FIRST
        # =========================

        unique.sort(
            key=lambda x: x.get("publishedAt", ""),
            reverse=True
        )

        return unique

    except Exception as err:

        print("❌ GNews Error:", err)

        return []

