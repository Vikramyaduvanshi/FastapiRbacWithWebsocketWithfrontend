from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


database_url=DATABASE_URL = "postgresql://postgres:896825@localhost:5432/trading_signal_db"

engine=create_engine(database_url)

SessionLocal=sessionmaker(
autocommit=False,
autoflush=False,
bind=engine

)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally :
        db.close()    

  