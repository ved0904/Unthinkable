# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = "sqlite:///./support_bot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_query = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_conversation(session_id: str):
    db = SessionLocal()
    history = db.query(Conversation).filter(Conversation.session_id == session_id).order_by(Conversation.timestamp).all()
    db.close()
    return history

def add_to_conversation(session_id: str, user_query: str, bot_response: str):
    db = SessionLocal()
    new_entry = Conversation(
        session_id=session_id,
        user_query=user_query,
        bot_response=bot_response
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()
    return new_entry