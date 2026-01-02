from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class CoachAvailability(Base):
    __tablename__ = "coach_availability"

    availability_id = Column(Integer, primary_key=True, autoincrement=True)

    coach_id = Column(
        Integer,
        ForeignKey("coach_profile.coach_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    start_date_time = Column(DateTime(timezone=True), nullable=False)
    end_date_time = Column(DateTime(timezone=True), nullable=False)

    # simple flag you can use later when booking a coach slot
    is_booked = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    coach = relationship("CoachProfile", back_populates="availabilities")

    __table_args__ = (
        CheckConstraint(
            "end_date_time > start_date_time",
            name="ck_coach_availability_end_after_start",
        ),
    )

    def __repr__(self) -> str:
        return f"<CoachAvailability id={self.availability_id} coach_id={self.coach_id} start={self.start_date_time}>"
