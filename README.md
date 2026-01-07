# Wellness Accountability App

A personal wellness + accountability app I’m building to track habit consistency and support an “accountability buddy” workflow (User + Coach + Admin roles). Really just my roomate for now haha...

## Current Status
- Backend foundation is complete: PostgreSQL + SQLAlchemy models, Alembic migrations, Dockerized DB, and seed/demo data.
- Frontend/UI is a work in progress (currently has layout/UX issues being cleaned up).

## Planned Work
- Finish building and test FastAPI endpoints for core flows (create sessions, commit/join, mark complete, history).
- Add a React/Next.js frontend for dashboards and session tracking (fix bugs) 
- Deploy on AWS (ECS Fargate) when the API + UI are stable (the most exciting bit lets be honest!)
