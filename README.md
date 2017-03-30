# Massachusetts-Bay-Transit-Authority
MSD Repo for CS4500 Spring 2017

## Configuration
To establish a database connection, first rename the "alembic.ini.EXAMPLE" file to "alembic.ini".
In the "alembic.ini" file, set sqlalchemy.url = postgresql://user:pass@localhost/dbname

Set the environment variable PYTHONPATH to the top level directory "Massachusetts-Bay-Transit-Authority-1", so that
Alembic database migration scripts can run.

## Development
This project relies on at least python 3.4.

To activate the virtual environment run `source ./bin/activate.sh` from the project root.
This should:
- Check that you are using the correct python version.
- Create the virtual environment if it doesn't exist.
- Install dependencies listed in requirements.txt
- Activate the virtual environment

## Migration
To upgrade to the latest database version run "alembic upgrade head".

## Testing
This project uses the nose testing framework, which should discover your tests automagically.

To run the project tests, run `nose2`.

