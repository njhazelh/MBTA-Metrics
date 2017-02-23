import configparser
import logging
import sqlalchemy

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# read from settings file
config = configparser.ConfigParser()
config.read("settings.cfg")
user = config.get('Database', 'user')
passwd = config.get('Database', 'pass')

# set up connection
engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd +'@localhost:5432/postgres')
connection = engine.connect()




