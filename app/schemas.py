# Pydantic schemas for request/response validation
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EscalationCheckRequest(BaseModel):
    """Request schema for checking if a conversation needs escalation"""
    ticket_id: str
    conversation: str


class EscalationCheckResponse(BaseModel):
    """Response schema after checking escalation"""
    ticket_id: str
    escalate: bool
    reason: str
    log_id: int


class EscalationLogResponse(BaseModel):
    """Response schema for escalation log entries"""
    id: int
    ticket_id: str
    escalate: bool
    reason: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EscalationStatsResponse(BaseModel):
    """Response schema for escalation statistics"""
    total: int
    escalated: int
    not_escalated: int
    escalation_rate: float


class HealthResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str
    db: str
    llm: str
