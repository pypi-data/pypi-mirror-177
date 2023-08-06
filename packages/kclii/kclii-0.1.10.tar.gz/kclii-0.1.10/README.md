# K CLI

Create migration

alembic revision --autogenerate -m "init"

Upgrade to the latest version

alembic upgrade head 

Downgrade

alembic downgrade base

check history

alembic history