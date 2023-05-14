# Creating Social Media Rest Api Using Fast Api

<br>

## 🖥️ Tech Stack

1. Python
2. FastApi
3. PostgresSql
4. Pydantic
5. Alembic
6. Docker
7. Docker Compose

**PostgresSql has a limitation, it does not migrate database once table is created, So we use alembic that help to migrate on every changes in postgresSql. models**

**NOTE :- Pydantic help to validate data using python.**

<br>

## Getting Started

    Create vitual env
        Command:-
            python3 -m venv <NameOfYourEnvironment>

    Install fast api
        Command:-
            pip install fastapi[all]

    Install 'psycopg2-binary'
    This is a postgresql database adapter that will connect to your postgressql database
        Command:-
            pip install psycopg2-binary

    install 'sqlalchemy'
    This is a python SQL toolkit and ORM(Object Relational Mapper) that gives you flexibility to wirte sql query and defining models
        command:-
            pip install sqlalchemy

## To run locally

    Use Command:-
        uvicorn app.main:app --reload

    This command will continuously check if anything you do changes in your file.
