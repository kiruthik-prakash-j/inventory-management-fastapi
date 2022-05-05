# Installation and Setup Guide


## Initialize the Folder
```
git clone https://github.com/kiruthik-prakash-j/inventory-management-fastapi.git
```

## Initialze the Python virtual Environment

### For Windows:
```
# Set up the Virtual Environment:
py -3 -m venv venv

# To use the Virtual Environment:
venv\Scripts\activate.bat
```

### For Linux and Mac:
```
# To set up the Virtual Environment
python3 -m venv venv

# To use the Virtual Environment
source venv/bin/activate
```

## Install PostgreSQL:

Download and install PostgreSQL from the below link:

[https://www.postgresql.org/download/](https://www.postgresql.org/download/)


## Install Dependencies:
```
pip install "fastapi[all]"
```

## Install psycopg2 library
```
pip install psycopg2
```

## Install SQLAlchemy
```
pip install sqlalchemy
```

## Install passlib
```
pip install "passlib[bcrypt]"
```

## Install python-jose
```
pip install "python-jose[cryptography]"
```

## Set the Environment Variables

Create a File `.env` and insert the following details in it:
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=<database_password>
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=<secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

## Install alembic:

```
pip install alembic
alembic init
alembic revision --autogenerate -m "Alembic Revision"
```

## Run the app
```
uvicorn app.main:app --reload
```

## Setting up Heroku

Go to the below website and download and install Heroku:

[https://devcenter.heroku.com/articles/getting-started-with-python#set-up](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

Login to heroku:
```
heroku login
```

Create a heroku app with a unique name:
```
heroku create <unique-app-name>
```
