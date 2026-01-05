from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class WellnessSession(Base):
    __tablename__ = "wellness_session"

    session_id = Column(Integer, primary_key=True, autoincrement=True)

    # replaces session_type: HABIT (individual) or GROUP (event)
    session_kind = Column(String(10), nullable=False)

    start_date_time = Column(DateTime, nullable=False)
    end_date_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)

    # foreign keys
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)
    created_by_admin_id = Column(Integer, ForeignKey("admin_profile.admin_id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coach_profile.coach_id"), nullable=True)

    # for HABIT sessions, user_id should be set; for GROUP events it should be NULL
    user_id = Column(Integer, ForeignKey("user_profile.user_id"), nullable=True)

    # relationships (defined on the base so both HABIT/GROUP inherit them)
    location = relationship("Location", back_populates="sessions")
    coach = relationship("CoachProfile", back_populates="sessions")
    user = relationship("UserProfile", back_populates="sessions")
    created_by_admin = relationship("AdminProfile", back_populates="group_events_created")

    __table_args__ = (
        CheckConstraint(
            "session_kind IN ('HABIT','GROUP')",
            name="ck_wellness_session_kind",
        ),
        CheckConstraint(
            "max_capacity > 0",
            name="ck_wellness_session_max_capacity_positive",
        ),
        CheckConstraint(
            "end_date_time > start_date_time",
            name="ck_wellness_session_end_after_start",
        ),
        CheckConstraint(
            "(session_kind = 'HABIT' AND user_id IS NOT NULL) OR (session_kind = 'GROUP' AND user_id IS NULL)",
            name="ck_wellness_session_user_by_kind",
        ),
    )

    __mapper_args__ = {"polymorphic_on": session_kind}

    def __repr__(self) -> str:
        return f"<WellnessSession id={self.session_id} kind={self.session_kind} start={self.start_date_time}>"