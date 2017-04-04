# Massachusetts-Bay-Transit-Authority
MSD Repo for CS4500 Spring 2017

## Configuration
To establish a database connection, first rename the `alembic.ini.EXAMPLE` file to `alembic.ini`.
In `alembic.ini`, set `sqlalchemy.url = postgresql://<user>:<pass>@<host>/<dbname>`

Set the environment variable `PYTHONPATH` to the top level directory
`Massachusetts-Bay-Transit-Authority-1`, so that Alembic database migration scripts can run.

## Development
This project relies on at least python 3.4.

To activate the virtual environment run `source ./bin/activate.sh` from the project root.
This should:
- Check that you are using the correct python version.
- Create the virtual environment if it doesn't exist.
- Install dependencies listed in requirements.txt
- Activate the virtual environment

There is a Makefile to aid development.  It's features may change but at the moment it can:
- `make lint # Run python linter`
- `make test # Run python unittests`
- `make run <module> <args...> # Runs python -m mbtaalerts.<module> <args...>`
- `make freeze # freeze dependencies to requirements.txt`
- `make install # Runs the active.sh script, although it won't source`

**You don't need to active the python environment for this to work**

## Migration
To upgrade to the most recent version of the database schema.
```bash
cd Massachusetts-Bay-Transit-Authority-1
export PYTHONPATH=`pwd`
cd mbtaalerts
CONFIG="../settings.cfg" alembic upgrade head
```

## Testing
This project uses NoseTests2 to automatically discover unittests.  You can run this manually
using `nose2` or using the Makefile `make test`.
