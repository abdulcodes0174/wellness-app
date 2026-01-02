from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db.base import Base


class CoachProfile(Base):
    __tablename__ = "coach_profile"

    # primary key and attributes
    coach_id = Column(Integer, primary_key=True, autoincrement=True)

    gender = Column(String(20))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # date of birth (year/month/day)
    birth_year = Column(Integer)
    birth_month = Column(Integer)
    birth_day = Column(Integer)

    email = Column(String(255), nullable=False, unique=True)

    # coach has one-to-many relationship to CoachAvailability
    availabilities = relationship("CoachAvailability", back_populates="coach")

    # coach has one-to-many relationship to HabitSession (guided 1:1 sessions)
    habit_sessions = relationship("HabitSession", back_populates="coach")

    # linking to account
    account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False, unique=True)
    account = relationship("Account", back_populates="coach_profile")

    __table_args__ = (
        CheckConstraint(
            "gender IN ('Male','Female','Other','Prefer not to say')",
            name="ck_coach_profile_gender",
        ),
    )

    def __repr__(self) -> str:
        return f"<CoachProfile id={self.coach_id} name={self.first_name} {self.last_name}>"