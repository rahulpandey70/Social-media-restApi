# Creating Social Media Rest Api Using Fast Api

    In this rest api i'm using FastApi and Postgres Database to store data.

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
    This is a python SQL toolkit and ORM(Object Relational Mapper) that gives you flexibility to wirte sql query
        command:-
            pip install sqlalchemy

## To run locally

    Use Command:-
        uvicorn app.main:app --reload

    This command will continuously check if anything you do changes in your file.
