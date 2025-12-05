"""
SQLAlchemy database models for activities and participants.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Activity(Base):
    """Model representing an extracurricular activity."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to participants
    participants = relationship("Participant", back_populates="activity", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": [p.email for p in self.participants],
            "current_participants": len(self.participants),
        }


class Participant(Base):
    """Model representing a student signed up for an activity."""
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    signed_up_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to activity
    activity = relationship("Activity", back_populates="participants")

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "email": self.email,
            "activity_id": self.activity_id,
            "signed_up_at": self.signed_up_at.isoformat() if self.signed_up_at else None,
        }
