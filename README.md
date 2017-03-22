# Massachusetts-Bay-Transit-Authority
MSD Repo for CS4500 Spring 2017

## Configuration
To establish a database connection, first rename the "settings.cfg.EXAMPLE" file to "settings.cfg".
Under the Database section of "settings.cfg", change the values to your user/pass pair, etc. 

## Development
This project relies on at least python 3.4.

To activate the virtual environment run `source ./bin/activate.sh` from the project root.
This should:
- Check that you are using the correct python version.
- Create the virtual environment if it doesn't exist.
- Install dependencies listed in requirements.txt
- Activate the virtual environment

## Testing
This project uses the nose testing framework, which should discover your tests automagically.

To run the project tests, run `nose2`.

