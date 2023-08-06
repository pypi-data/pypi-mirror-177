# K CLI

Create migration

alembic revision --autogenerate -m "init"

Upgrade to the latest version

alembic upgrade head 

Downgrade

alembic downgrade base

check history

alembic history


## Chmod

sudo kinit
sudo chmod +x /usr/local/bin/koff
sudo chmod +x /usr/local/bin/kon

## Create alias

alias koff=source /usr/local/bin/koff
alias kon=source /usr/local/bin/kon