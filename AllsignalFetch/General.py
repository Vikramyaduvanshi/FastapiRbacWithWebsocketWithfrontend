from fastapi import APIRouter, Depends
from Database.ds import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from Models.md import TradingSignal

allsignalrouter = APIRouter(
    prefix="/general",
    tags=["general"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@allsignalrouter.get("/all_signals")
async def get_all_signals(db: db_dependency):

    alldata = db.query(TradingSignal).all()

    return {"message": "all data fetched", "allsignal": alldata}