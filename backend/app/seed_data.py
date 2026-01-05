# backend/app/seed_data.py

import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models.account import Account
from app.models.admin_profile import AdminProfile
from app.models.coach_profile import CoachProfile
from app.models.user_profile import UserProfile
from app.models.location import Location
from app.models.coach_availability import CoachAvailability
from app.models.habit_session import HabitSession
from app.models.group_event import GroupEvent
from app.models.commitment import Commitment


def _safe_kwargs(Model, **kwargs):
    """
    Only pass fields that actually exist on the SQLAlchemy model.
    This makes the seed script resilient if we later remove columns like `email`
    from profiles (because Account becomes the source of truth).
    """
    return {k: v for k, v in kwargs.items() if hasattr(Model, k)}


def seed_data():
    load_dotenv()
    db_url = os.environ["DATABASE_URL"]

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)

    now = datetime.now(timezone.utc)
    day1 = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Times (tomorrow)
    group_start = day1.replace(hour=18, minute=0)   # 6:00 PM
    group_end = day1.replace(hour=19, minute=0)     # 7:00 PM

    habit_start = day1.replace(hour=19, minute=30)  # 7:30 PM
    habit_end = day1.replace(hour=20, minute=0)     # 8:00 PM

    avail_start = day1.replace(hour=17, minute=0)   # 5:00 PM
    avail_end = day1.replace(hour=21, minute=0)     # 9:00 PM

    # Demo emails (change anytime)
    admin_email = "admin@wellness.local"
    coach_email = "raj.b@wellness.local"
    user_email = "me@wellness.local"

    # NOTE: These are demo hashes (NOT real hashing). Replace later with real auth.
    demo_hash = "demo_hash_not_secure"

    with SessionLocal() as db:
        # Idempotency check: if admin account exists, assume seeded already
        existing = db.execute(select(Account).where(Account.email == admin_email)).scalar_one_or_none()
        if existing is not None:
            print("Seed data already present; skipping.")
            return

        # --- Accounts ---
        admin_acc = Account(**_safe_kwargs(
            Account,
            email=admin_email,
            password_hash=demo_hash,
            role="ADMIN",
            is_active=True,
        ))
        coach_acc = Account(**_safe_kwargs(
            Account,
            email=coach_email,
            password_hash=demo_hash,
            role="COACH",
            is_active=True,
        ))
        user_acc = Account(**_safe_kwargs(
            Account,
            email=user_email,
            password_hash=demo_hash,
            role="USER",
            is_active=True,
        ))

        db.add_all([admin_acc, coach_acc, user_acc])
        db.flush()  # assigns account_ids

        # --- Profiles ---
        admin_profile = AdminProfile(**_safe_kwargs(
            AdminProfile,
            account_id=admin_acc.account_id,
            first_name="Wellness",
            last_name="Admin",
            phone_number="000-000-0000",
            email=admin_email,  # safe even if removed later (safe_kwargs handles it)
        ))

        # Your accountability buddy as coach
        coach_profile = CoachProfile(**_safe_kwargs(
            CoachProfile,
            account_id=coach_acc.account_id,
            first_name="Raj",
            last_name="B",
            gender="Male",
            birth_year=2000,
            birth_month=1,
            birth_day=1,
            email=coach_email,
        ))

        # You as user
        user_profile = UserProfile(**_safe_kwargs(
            UserProfile,
            account_id=user_acc.account_id,
            first_name="Me",
            last_name="User",
            gender="Male",
            birth_year=2000,
            birth_month=1,
            birth_day=1,
            phone_number="111-111-1111",
            email=user_email,
            current_weight=Decimal("82.50"),
            goal_weight=Decimal("78.00"),
        ))

        db.add_all([admin_profile, coach_profile, user_profile])
        db.flush()  # assigns profile IDs

        # --- Locations (contexts) ---
        home = Location(**_safe_kwargs(
            Location,
            location_name="Home",
            max_capacity=2,
            admin_id=admin_profile.admin_id,
        ))
        gym = Location(**_safe_kwargs(
            Location,
            location_name="Gym",
            max_capacity=10,
            admin_id=admin_profile.admin_id,
        ))
        db.add_all([home, gym])
        db.flush()

        # --- Coach availability ---
        avail = CoachAvailability(**_safe_kwargs(
            CoachAvailability,
            coach_id=coach_profile.coach_id,
            start_date_time=avail_start,
            end_date_time=avail_end,
            is_booked=False,
        ))
        db.add(avail)
        db.flush()

        # --- Sessions ---
        # Group event coached by Raj, hosted at Gym (no specific user_id for GROUP)
        group_event = GroupEvent(**_safe_kwargs(
            GroupEvent,
            start_date_time=group_start,
            end_date_time=group_end,
            max_capacity=5,
            location_id=gym.location_id,
            created_by_admin_id=admin_profile.admin_id,
            coach_id=coach_profile.coach_id,
            user_id=None,  # must be NULL for GROUP if you used that constraint
        ))

        # Habit session for you, with Raj as accountability coach, hosted at Home
        habit_session = HabitSession(**_safe_kwargs(
            HabitSession,
            start_date_time=habit_start,
            end_date_time=habit_end,
            max_capacity=1,
            location_id=home.location_id,
            created_by_admin_id=admin_profile.admin_id,
            coach_id=coach_profile.coach_id,
            user_id=user_profile.user_id,  # must be set for HABIT if you used that constraint
        ))

        db.add_all([group_event, habit_session])
        db.flush()

        # --- Commitment: you join the group event ---
        join = Commitment(**_safe_kwargs(
            Commitment,
            user_id=user_profile.user_id,
            session_id=group_event.session_id,
            status="PLANNED",
            note="Accountability session with Raj B",
        ))
        db.add(join)

        db.commit()
        print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed_data()
