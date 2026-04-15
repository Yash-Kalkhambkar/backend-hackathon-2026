# SQLAlchemy database models
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class EscalationLog(Base):
    """Model for escalation_logs table - matches existing database schema"""
    __tablename__ = "escalation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String)
    conversation = Column(Text)
    escalate = Column(Boolean)
    reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
