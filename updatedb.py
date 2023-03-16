
from refresher import refresher
from sqlalchemy import (
    create_engine,
    Integer, String,
    Table, Column,
    MetaData, inspect,
    insert, select, 
    update, Engine,
)
import json

# glob variables
CONFIG:dict = None
ENGINE:Engine = None
TABLE:Table = None

def load_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        global CONFIG
        CONFIG = json.load(file)

def init_db():
    global ENGINE
    global TABLE
    
    ENGINE = create_engine(CONFIG['connect_str'], future=True)
    TableName = "pixiv_token"
    
    metadata = MetaData()
    TABLE = Table(
        TableName,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("access_token", String(50), nullable=False),
        Column("refresh_token", String(50), nullable=False),
        Column("expires_in", Integer, nullable=False),
        Column("refresh_at", Integer, nullable=False),
    )
    if not inspect(ENGINE).has_table(TableName):  # If table don't exist, Create.
        metadata.create_all(ENGINE)

def insert_or_update_token(token, old_token:dict=None):
    global ENGINE
    global TABLE
    
    validate = select(TABLE).where(
        TABLE.c.refresh_token == token['refresh_token']
    )
    compiled = validate.compile()
    has_row = False
    with ENGINE.connect() as conn:
        result = conn.execute(validate)
        has_row = result.first() is not None
        # conn.commit()
    
    if has_row and old_token is not None:
        set_token = update(TABLE).values(
            access_token = token['access_token'],
            refresh_token = token['refresh_token'],
            expires_in = token['expires_in'],
            refresh_at = token['refresh_at'],
        ).where(
            TABLE.c.refresh_token == old_token['refresh_token']
        )
    else:
        set_token = insert(TABLE).values(
            access_token = token['access_token'],
            refresh_token = token['refresh_token'],
            expires_in = token['expires_in'],
            refresh_at = token['refresh_at'],
        )
    
    compiled = set_token.compile()
    with ENGINE.connect() as conn:
        result = conn.execute(set_token)
        conn.commit()

def main():
    try:
        load_config()
        init_db()
        ref = refresher()
        old_token = ref.get_token()
        new_token = ref.do_refresh()
        insert_or_update_token(new_token, old_token)
    except Exception as err:
        print(f'Exception: {err}')
        exit(-1)


if __name__ == '__main__':
    main()

