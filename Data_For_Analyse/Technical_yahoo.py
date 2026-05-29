
import yfinance as yf
from ta.trend import (
    SMAIndicator,
    EMAIndicator,
    MACD,
    ADXIndicator
)

from ta.momentum import RSIIndicator

from ta.volatility import (
    AverageTrueRange,
    BollingerBands
)


# ==========================================
# FOREX SYMBOL FORMATTER
# ==========================================

def format_forex_symbol(symbol):

    symbol_map = {

        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "JPY=X",
        "USDCHF": "CHF=X",
        "AUDUSD": "AUDUSD=X",
        "NZDUSD": "NZDUSD=X",
        "USDCAD": "CAD=X",
        "USDINR": "INR=X",
        "XAUUSD": "GC=F",
        "XAGUSD": "SI=F",
        "BTCUSD": "BTC-USD",
        "ETHUSD": "ETH-USD",
    }

    clean = symbol.replace("/", "").upper()

    return symbol_map.get(clean, clean)


# ==========================================
# SAFE FLOAT
# ==========================================

def safe_float(value):

    try:

        return round(float(value), 5)

    except:

        return 0.0


# ==========================================
# MAIN FUNCTION
# ==========================================

async def forex_technical_data(
    input_symbol="EURUSD"
):

    try:

        # ==========================================
        # SYMBOL
        # ==========================================

        symbol = format_forex_symbol(
            input_symbol
        )

        # ==========================================
        # DOWNLOAD DATA
        # ==========================================

        df = yf.download(

            symbol,

            start="2024-01-01",

            interval="1d",

            progress=False,

            auto_adjust=True
        )

        # ==========================================
        # VALIDATION
        # ==========================================

        if df.empty or len(df) < 250:

            return {

                "error": True,

                "message": "Not enough data"
            }

        # ==========================================
        # FIX SERIES ISSUE
        # ==========================================

        close = df["Close"].squeeze()

        high = df["High"].squeeze()

        low = df["Low"].squeeze()

        # ==========================================
        # CURRENT PRICE
        # ==========================================

        current_price = safe_float(
            close.iloc[-1]
        )

        # ==========================================
        # SMA
        # ==========================================

        sma50 = safe_float(

            SMAIndicator(
                close=close,
                window=50
            ).sma_indicator().iloc[-1]
        )

        sma200 = safe_float(

            SMAIndicator(
                close=close,
                window=200
            ).sma_indicator().iloc[-1]
        )

        # ==========================================
        # EMA
        # ==========================================

        ema20 = safe_float(

            EMAIndicator(
                close=close,
                window=20
            ).ema_indicator().iloc[-1]
        )

        ema50 = safe_float(

            EMAIndicator(
                close=close,
                window=50
            ).ema_indicator().iloc[-1]
        )

        # ==========================================
        # RSI
        # ==========================================

        rsi = safe_float(

            RSIIndicator(
                close=close,
                window=14
            ).rsi().iloc[-1]
        )

        # ==========================================
        # MACD
        # ==========================================

        macd_obj = MACD(close)

        macd_line = safe_float(
            macd_obj.macd().iloc[-1]
        )

        macd_signal_line = safe_float(
            macd_obj.macd_signal().iloc[-1]
        )

        macd_signal = (

            "Bullish"

            if macd_line > macd_signal_line

            else "Bearish"
        )

        # ==========================================
        # ATR
        # ==========================================

        atr = safe_float(

            AverageTrueRange(

                high=high,

                low=low,

                close=close,

                window=14

            ).average_true_range().iloc[-1]
        )

        # ==========================================
        # ADX
        # ==========================================

        adx = safe_float(

            ADXIndicator(

                high=high,

                low=low,

                close=close,

                window=14

            ).adx().iloc[-1]
        )

        # ==========================================
        # BOLLINGER BANDS
        # ==========================================

        bb = BollingerBands(

            close=close,

            window=20,

            window_dev=2
        )

        bb_upper = safe_float(
            bb.bollinger_hband().iloc[-1]
        )

        bb_middle = safe_float(
            bb.bollinger_mavg().iloc[-1]
        )

        bb_lower = safe_float(
            bb.bollinger_lband().iloc[-1]
        )

        # ==========================================
        # VOLATILITY
        # ==========================================

        volatility = "Low"

        atr_percent = (
            atr / current_price
        ) * 100 if current_price else 0

        if atr_percent > 1:

            volatility = "High"

        elif atr_percent > 0.5:

            volatility = "Moderate"

        # ==========================================
        # TREND
        # ==========================================

        trend = "Sideways"

        if (
            current_price > sma50 and
            sma50 > sma200 and
            ema20 > ema50
        ):

            trend = "Strong Bullish"

        elif current_price > sma50:

            trend = "Bullish"

        elif (
            current_price < sma50 and
            sma50 < sma200
        ):

            trend = "Strong Bearish"

        elif current_price < sma50:

            trend = "Bearish"

        # ==========================================
        # MOMENTUM
        # ==========================================

        momentum = "Neutral"

        if (
            rsi > 60 and
            macd_signal == "Bullish"
        ):

            momentum = "Strong Bullish"

        elif (
            rsi < 40 and
            macd_signal == "Bearish"
        ):

            momentum = "Strong Bearish"

        # ==========================================
        # MARKET STATE
        # ==========================================

        market_state = "Range Bound"

        if (
            adx > 25 and
            "Bullish" in trend
        ):

            market_state = "Bullish Trend"

        elif (
            adx > 25 and
            "Bearish" in trend
        ):

            market_state = "Bearish Trend"

        # ==========================================
        # TECHNICAL BIAS
        # ==========================================

        technical_bias = "NEUTRAL"

        if (
            "Bullish" in trend and
            macd_signal == "Bullish" and
            rsi > 50
        ):

            technical_bias = "BUY"

        elif (
            "Bearish" in trend and
            macd_signal == "Bearish" and
            rsi < 50
        ):

            technical_bias = "SELL"

        # ==========================================
        # SUPPORT / RESISTANCE
        # ==========================================

        recent_high = safe_float(
            high.tail(20).max()
        )

        recent_low = safe_float(
            low.tail(20).min()
        )

        # ==========================================
        # RISK SENTIMENT
        # ==========================================

        risk_sentiment = "Neutral"

        if (
            "JPY" in input_symbol or
            "CHF" in input_symbol
        ):

            risk_sentiment = (
                "Safe Haven Sensitive"
            )

        elif (
            "AUD" in input_symbol or
            "NZD" in input_symbol
        ):

            risk_sentiment = (
                "Risk-On Sensitive"
            )

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return {

            "pair":
                input_symbol.upper(),

            "yahooSymbol":
                symbol,

            "currentPrice":
                current_price,

            "trend":
                trend,

            "marketState":
                market_state,

            "technicalBias":
                technical_bias,

            "momentum":
                momentum,

            "volatility":
                volatility,

            "riskSentiment":
                risk_sentiment,

            "indicators": {

                "rsi": rsi,

                "macd":
                    macd_signal,

                "adx": adx,

                "atr": atr,

                "sma50": sma50,

                "sma200": sma200,

                "ema20": ema20,

                "ema50": ema50,
            },

            "bollingerBands": {

                "upper":
                    bb_upper,

                "middle":
                    bb_middle,

                "lower":
                    bb_lower,
            },

            "supportResistance": {

                "resistance":
                    recent_high,

                "support":
                    recent_low,
            },

            "summary":

                f"{input_symbol.upper()} is in "
                f"{trend} trend with "
                f"{momentum} momentum. "
                f"MACD is {macd_signal}. "
                f"RSI is {rsi}. "
                f"ADX is {adx}. "
                f"Volatility is {volatility}."
        }

    except Exception as error:

        print(
            "❌ Technical Error:",
            str(error)
        )

        return {

            "error": True,

            "message": str(error)
        }

