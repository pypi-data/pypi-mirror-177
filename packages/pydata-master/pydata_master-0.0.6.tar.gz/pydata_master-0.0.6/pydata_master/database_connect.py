# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.

import pandas as pd
import psycopg2 as ps
from configparser import ConfigParser
from sqlalchemy import create_engine

# DATABASE CONFIG
def db_config(section, db_cred_path):
    """
    Load credentials by a specific item name
    Args:
        item_name (:obj:`str`, required): name of the item that needs to load its value
        cred_path (:obj:`str`, required): Path to the .ini file where credentials are located.
    """
    parser = ConfigParser()
    parser.read(db_cred_path)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, db_cred_path))
    return db

def db_query(query, section, db_cred_path):
  db_cred = db_config(section, db_cred_path)
  db_uri = 'postgresql://{}:{}@{}:{}/{}'.format(db_cred['user'], db_cred['password'], db_cred['host'], db_cred['port'], db_cred['database'])
  engine = create_engine(db_uri)
  try:
    query_result = pd.read_sql(query, engine)
    return query_result
  except (Exception, ps.DatabaseError) as error:
    print(error)

