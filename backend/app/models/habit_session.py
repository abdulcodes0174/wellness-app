from app.models.wellness_session import WellnessSession


class HabitSession(WellnessSession):
    __mapper_args__ = {"polymorphic_identity": "HABIT"}