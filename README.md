# Creating Social Media Rest Api Using Fast Api

## 🖥️ Tech Stack

<a href="https://discord.gg/EHthxHRUmr">
    <img src="https://skillicons.dev/icons?i=python,fastapi,postgresql,docker" />
  </a>

<br>

**PostgresSql has a limitation, it does not migrate database once table is created, So we use alembic that help to migrate on every changes in postgresSql. models**

**NOTE :- Pydantic help to validate data using python.**

<br>

## Getting Started

    Create vitual env
        Command:-
            python3 -m venv <NameOfYourEnvironment>

    Activate virtual env
        Command:-
            source venv/bin/activate

    Install all packages
        Command:-
            pip install -r requirements.txt

## To run locally

    Use Command:-
        uvicorn app.main:app --reload

    This command will continuously check if anything you do changes in your file.

## To run using docker compose

    Use Command:
        docker compose -f docker-compose-dev.yml up
