from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class AdminProfile(Base):
    __tablename__ = "admin_profile"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    phone_number = Column(String(20))
    email = Column(String(255), nullable=False, unique=True)

    # Admin manages locations/contexts
    locations = relationship("Location", back_populates="admin")

    # Admin can create group wellness events (or system-wide sessions)
    group_events_created = relationship("GroupEvent", back_populates="created_by_admin")

    # linking to account
    account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False, unique=True)
    account = relationship("Account", back_populates="admin_profile")


    def __repr__(self) -> str:
        return f"<AdminProfile id={self.admin_id} name={self.first_name} {self.last_name}>"