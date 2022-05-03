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

## Install Dependencies:
```
pip install "fastapi[all]"
```

## Run the app
```
uvicorn app.main:app --reload
```

## Database and Tables:

Create Database using the Query
```
CREATE DATABASE fastapi
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
```

Create Table with the Query
```
CREATE TABLE public."Items"
(
    id serial NOT NULL,
    name character varying,
    quantity integer NOT NULL DEFAULT 0,
    "row" integer NOT NULL,
    "column" integer NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."Items"
    OWNER to postgres;
```

## Install psycopg2 library
```
pip install psycopg2
```

## Install SQLAlchemy
```
pip install sqlalchemy
```