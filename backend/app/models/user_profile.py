from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db.base import Base



class UserProfile(Base):
    __tablename__ = "user_profile"

    # primary key and attributes
    user_id = Column(Integer, primary_key=True, autoincrement=True)

    # wellness-related attributes (kept from original, just renamed)
    goal_weight = Column(Numeric(5, 2))
    current_weight = Column(Numeric(5, 2))

    gender = Column(String(20), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # date of birth (year/month/day)
    birth_year = Column(Integer)
    birth_month = Column(Integer)
    birth_day = Column(Integer)

    phone_number = Column(String(20), unique=True)
    email = Column(String(255), nullable=False, unique=True)

    __table_args__ = (
        CheckConstraint(
            "goal_weight IS NULL OR goal_weight > 0",
            name="ck_user_profile_goal_weight_positive",
        ),
        CheckConstraint(
            "current_weight IS NULL OR current_weight > 0",
            name="ck_user_profile_current_weight_positive",
        ),
        CheckConstraint(
            "gender IN ('Male','Female','Other','Prefer not to say')",
            name="ck_user_profile_gender",
        ),
    )

    # A user can have many scheduled habit sessions
    habit_sessions = relationship("HabitSession", back_populates="user")
    # Tracks a user's participation in group wellness events (planned/completed/missed/canceled)
    commitments = relationship("Commitment", back_populates="user")


    # linking to account 
    account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False, unique=True)
    account = relationship("Account", back_populates="user_profile")

    def __repr__(self) -> str:
        return f"<UserProfile id={self.user_id} name={self.first_name} {self.last_name}>"