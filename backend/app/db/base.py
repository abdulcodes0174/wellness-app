from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models so they register with Base.metadata
from app.models.account import Account  # noqa: F401
from app.models.user_profile import UserProfile  # noqa: F401
from app.models.coach_profile import CoachProfile  # noqa: F401
from app.models.admin_profile import AdminProfile  # noqa: F401
from app.models.location import Location  # noqa: F401
from app.models.wellness_session import WellnessSession  # noqa: F401
from app.models.habit_session import HabitSession  # noqa: F401
from app.models.group_event import GroupEvent  # noqa: F401
from app.models.coach_availability import CoachAvailability  # noqa: F401
from app.models.commitment import Commitment  # noqa: F401