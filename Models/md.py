import enum
from sqlalchemy import Column, String, Float, DateTime,Enum,Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from Database.ds import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password = Column(String)
    isactive = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
  
    
   
  
class TradingSignal(Base):
    __tablename__ = "trading_signals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    target_price = Column(Float, nullable=False)
    entry_time = Column(DateTime(timezone=True), nullable=False)
    expiry_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="OPEN")
    realized_roi = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True),server_default=func.now())