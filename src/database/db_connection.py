
import sys


from configparser import ConfigParser
from pathlib import Path


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


path_to_config = Path(__file__).parent.parent.parent.joinpath('config.ini')
print('Path to DB CONFIGURATION.INI:::> ' + str(path_to_config))
db_configurations = ConfigParser()
db_configurations.read(path_to_config)

db_engine = db_configurations.get('DEV', 'engine')
db_username = db_configurations.get('DEV', 'username')
db_password = db_configurations.get('DEV', 'password')
db_host = db_configurations.get('DEV', 'host')
db_port = db_configurations.get('DEV', 'port')
db_name = db_configurations.get('DEV', 'db_name')

url_to_db = f'{db_engine}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
print(url_to_db)

engine = create_engine(url_to_db, echo=True,
pool_size=5)  # poetry add psycopg2 - установить драйвер для движка postgresql!
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()





