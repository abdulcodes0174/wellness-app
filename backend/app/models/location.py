from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Location(Base):
    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(100), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    # who manages/created this location (admin)
    admin_id = Column(Integer, ForeignKey("admin_profile.admin_id"), nullable=False)

    admin = relationship("AdminProfile", back_populates="locations")

    # a location can host many scheduled items (habit sessions + group events)
    sessions = relationship("WellnessSession", back_populates="location")

    __table_args__ = (
        CheckConstraint("max_capacity > 0", name="ck_location_max_capacity_positive"),
    )

    def __repr__(self) -> str:
        return f"<Location id={self.location_id} name={self.location_name}>"