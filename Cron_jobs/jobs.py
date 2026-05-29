from datetime import datetime, timezone
from sqlalchemy.orm import Session

from Models.md import TradingSignal
from Data_For_Analyse.Technical_yahoo import forex_technical_data


async def cronejob(db: Session):

    try:

        signals = db.query(TradingSignal).filter(TradingSignal.status == "OPEN").all()

        for signal in signals:

            technical_data = await forex_technical_data(signal.symbol)

            currentprice = technical_data.get("currentPrice")

            if currentprice is None:
                continue

            if signal.target_price > signal.entry_price and currentprice >= signal.target_price:
                signal.status = "TARGET_HIT"

            elif signal.target_price > signal.entry_price and currentprice <= signal.stop_loss:
                signal.status = "STOPLOSS_HIT"

    

            elif signal.target_price < signal.entry_price and currentprice >= signal.stop_loss:
                signal.status = "STOPLOSS_HIT"


            elif signal.target_price < signal.entry_price and currentprice <= signal.target_price:
                signal.status = "TARGET_HIT"


            if signal.target_price > signal.entry_price:

                signal.realized_roi = (
                    (
                        currentprice - signal.entry_price
                    ) / signal.entry_price
                ) * 100

            else:

                signal.realized_roi = (
                    (
                        signal.entry_price - currentprice
                    ) / signal.entry_price
                ) * 100


            current_time = datetime.now(timezone.utc)

            if signal.status == "OPEN" and current_time > signal.expiry_time:

                signal.status = "EXPIRED"
                
        db.commit()        

            

    except Exception as e:

        print(
            "Cron Job Error:",
            str(e)
        )