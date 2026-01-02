from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, autoincrement=True)

    # login identity (single source of truth for email + auth)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    # role-based access
    role = Column(String(10), nullable=False)  # USER / COACH / ADMIN
    is_active = Column(Boolean, nullable=False, default=True)

    # audit fields (for portfolio + admin)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # one-to-one optional links to profiles
    user_profile = relationship("UserProfile", back_populates="account", uselist=False)
    coach_profile = relationship("CoachProfile", back_populates="account", uselist=False)
    admin_profile = relationship("AdminProfile", back_populates="account", uselist=False)

    __table_args__ = (
        CheckConstraint("role IN ('USER','COACH','ADMIN')", name="ck_account_role"),
    )

    def __repr__(self) -> str:
        return f"<Account id={self.account_id} role={self.role} email={self.email}>"