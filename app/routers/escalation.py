# API endpoints for escalation detection
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import EscalationLog
from app.schemas import (
    EscalationCheckRequest,
    EscalationCheckResponse,
    EscalationLogResponse,
    EscalationStatsResponse,
    HealthResponse
)
from app.services.llm import check_escalation
from app.config import settings

router = APIRouter(prefix="/escalation", tags=["escalation"])


@router.post("/check", response_model=EscalationCheckResponse)
def check_escalation_endpoint(request: EscalationCheckRequest, db: Session = Depends(get_db)):
    """
    Accept a support conversation and ticket ID, call LLM to decide if escalation is needed,
    store the decision in database, and return the result.
    """
    # Call LLM service to analyze the conversation
    llm_result = check_escalation(request.conversation)
    
    # Create new log entry in database
    log = EscalationLog(
        ticket_id=request.ticket_id,
        conversation=request.conversation,
        escalate=llm_result["escalate"],
        reason=llm_result["reason"]
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Return response with escalation decision
    return EscalationCheckResponse(
        ticket_id=request.ticket_id,
        escalate=llm_result["escalate"],
        reason=llm_result["reason"],
        log_id=log.id
    )


@router.get("/logs", response_model=List[EscalationLogResponse])
def get_all_logs(db: Session = Depends(get_db)):
    """
    Retrieve all escalation logs from database, ordered by most recent first.
    """
    logs = db.query(EscalationLog).order_by(EscalationLog.created_at.desc()).all()
    return logs


@router.get("/logs/{ticket_id}", response_model=List[EscalationLogResponse])
def get_logs_by_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all escalation logs for a specific ticket ID.
    """
    logs = db.query(EscalationLog).filter(
        EscalationLog.ticket_id == ticket_id
    ).order_by(EscalationLog.created_at.desc()).all()
    return logs


@router.get("/stats", response_model=EscalationStatsResponse)
def get_escalation_stats(db: Session = Depends(get_db)):
    """
    Calculate and return escalation statistics including total logs,
    escalated count, not escalated count, and escalation rate percentage.
    """
    total = db.query(EscalationLog).count()
    escalated = db.query(EscalationLog).filter(EscalationLog.escalate == True).count()
    not_escalated = total - escalated
    
    # Calculate escalation rate as percentage, handle division by zero
    escalation_rate = round((escalated / total * 100), 1) if total > 0 else 0.0
    
    return EscalationStatsResponse(
        total=total,
        escalated=escalated,
        not_escalated=not_escalated,
        escalation_rate=escalation_rate
    )


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify database connection and LLM configuration.
    """
    # Test database connection
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    # Check if LLM API key is configured
    llm_status = "configured" if settings.GROQ_API_KEY else "not configured"
    
    return HealthResponse(
        status="ok",
        db=db_status,
        llm=llm_status
    )
