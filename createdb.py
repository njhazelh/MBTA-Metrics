import configparser
import logging
import sqlalchemy

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# read from settings file
config = configparser.ConfigParser()
config.read("settings.cfg")

host = config.get('Database', 'host')
port = config.get('Database', 'port')
db = config.get('Database', 'db')
user = config.get('Database', 'user')
passwd = config.get('Database', 'pass')

# set up connection
engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd + '@'
                                  + host + ':' + port + '/' + db)
connection = engine.connect()




