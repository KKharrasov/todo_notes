TODO Application - REST API service based on Fast API

Get started:

1. Change variable SQLALCHEMY_DATABASE_URL in core.db to make a connection with database:
choose user, password, port, host and name of database

2. Init migrations with following commands:
>>> alembic init migrations
>>> alembic revision --autogenerate -m " {Comment} "
>>> alembic upgrade head

3. Start local uvicorn server with command:
>>> uvicorn main:app --reload

4. Add '/docs' to URL and use 'Authorize' OAuth2's button to use APIs
