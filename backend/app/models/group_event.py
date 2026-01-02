from app.models.wellness_session import WellnessSession
from sqlalchemy.orm import relationship



class GroupEvent(WellnessSession):
    __mapper_args__ = {"polymorphic_identity": "GROUP"}

    # Users join group events via Commitment records (capacity + attendance tracking)
    commitments = relationship("Commitment", back_populates="group_event")
