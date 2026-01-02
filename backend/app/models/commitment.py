from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Commitment(Base):
    __tablename__ = "commitment"

    commitment_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("user_profile.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # references the base session table so it works with polymorphism;
    # relationship below targets GroupEvent (subclass)
    session_id = Column(
        Integer,
        ForeignKey("wellness_session.session_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = Column(String(12), nullable=False, default="PLANNED")
    note = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    user = relationship("UserProfile", back_populates="commitments")
    group_event = relationship("GroupEvent", back_populates="commitments")

    __table_args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_commitment_user_session"),
        CheckConstraint(
            "status IN ('PLANNED','COMPLETED','MISSED','CANCELED')",
            name="ck_commitment_status",
        ),
    )

    def __repr__(self) -> str:
        return f"<Commitment id={self.commitment_id} user_id={self.user_id} session_id={self.session_id} status={self.status}>"