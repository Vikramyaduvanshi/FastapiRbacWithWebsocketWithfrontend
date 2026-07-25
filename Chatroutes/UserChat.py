from fastapi import APIRouter, WebSocket,Depends
import json
from datetime import datetime, timedelta,timezone
from sqlalchemy.orm import Session
from typing import Annotated
from LLM.User_intent import extract_forex_intent
from Data_For_Analyse.Technical_yahoo import forex_technical_data
from Data_For_Analyse.gnews import fetch_all_news
from LLM.Generate_signal import get_forex_ai_result
from Models.md import TradingSignal
from Database.ds import get_db
from Middleware.Websocket_role import websocket_current_user
chatrouter = APIRouter(
    prefix="/chat",
    tags=["chat"]
)   
db_dependency = Annotated[Session, Depends(get_db)]
admin_dependency=Annotated[dict,Depends(websocket_current_user(["admin"]))]

@chatrouter.websocket("/ws")
async def websocket_endpoint(ws: WebSocket,user:admin_dependency,db:db_dependency):
    print(user)

    await ws.accept()

    while True:

        try:

            data = await ws.receive_text()

            print(data, "message from frontend")

           

            res = await extract_forex_intent(data)

            print(res)



            await ws.send_text( "Fetching technical data from Yahoo...")

            technicaldata = await forex_technical_data(res.get("symbol"))

            print(technicaldata)

            await ws.send_text(json.dumps(technicaldata))



            newslist = []

            news = await fetch_all_news()

            for v in news:

                newslist.append(

                    {
                        "title":
                            v.get("title"),

                        "content":
                            v.get("content", "")[:200],

                        "source":
                            v.get("source", {}).get("name")
                    }
                )


            await ws.send_text( "AI is analyzing market conditions...")

            final = await get_forex_ai_result(technicaldata, newslist, {**res, "current_price": technicaldata.get("currentPrice")})

            roi=0

            if final.get("marketBias") == "BUY":
                    roi = (( technicaldata.get("currentPrice") - float(final.get("buyZone").split("-")[0]))/float(final.get("buyZone").split("-")[0]))

            else   :
                  
                  roi = (( float(final.get("sellZone").split("-")[0])    - technicaldata.get("currentPrice"))/float(final.get("sellZone").split("-")[0])) * 100

            await ws.send_text( json.dumps(final) )
           

            create_signal= TradingSignal(
                symbol=final.get("pair"),
                direction=final.get("trendStrength"),
                entry_price=float(final.get("buyZone").split("-")[0]),
                stop_loss=float(final.get("stopLoss")),
                target_price=float(final.get("takeProfit1")),
                entry_time=datetime.now(timezone.utc),
                expiry_time=datetime.now(timezone.utc) + timedelta(hours=4),
                status="OPEN",
                realized_roi=roi
            )

            db.add(create_signal)
            db.commit()




        except Exception as e:

            print("WebSocket Error:", str(e))

            await ws.send_text(

                json.dumps({
                    "error": str(e)
                })
            )