from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import model modules so they register with Base.metadata
import app.models.account  # noqa: F401
import app.models.admin_profile  # noqa: F401
import app.models.coach_profile  # noqa: F401
import app.models.user_profile  # noqa: F401
import app.models.location  # noqa: F401
import app.models.wellness_session  # noqa: F401
import app.models.coach_availability  # noqa: F401
import app.models.commitment  # noqa: F401

# Optional (only if these exist in your project)
import app.models.habit_session  # noqa: F401
import app.models.group_event  # noqa: F401
