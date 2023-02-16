from sqlite3 import Error, connect
from .classes.activity import Activity
from .classes.period import Period

def close_connection(conn):
    if conn:
        conn.close()

def create_connection():
    try:
        conn = connect('./weekplanner.db')
    except Error as e:
        print('Database error on connecting:')
        print(e)
    return conn

def execute_query(query, obj, error_message='', fetch=False):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, obj)
        if fetch == 1:
            return cursor.fetchone()
        elif fetch > 1:
            return cursor.fetchall()
    except Error as e:
        print(f'[Database error]{error_message}:')
        print(e)
    finally:
        close_connection(conn)

def create_database():
    with open('shared/sql/create_activity.sql') as f:
        execute_query(f.read(), [], 'creating tables')
    with open('shared/sql/create_period.sql') as f:
        execute_query(f.read(), [], 'creating tables')

def prepare_params(obj, conditions, exclude=[]):
    table = str(type(obj)).split('.')[-1:][0][:-2].lower()
    items = list(filter(lambda item: item[0] not in exclude, vars(obj).items()))
    keys = list(map(lambda item: item[0], items))
    values = []
    if conditions:
        values = list(map(
            lambda i: i[1],
            filter(lambda i: i[0] in conditions, items)))
    else:
        values = list(map(lambda i: i[1], items))
    # return (table, keys, values, items)

    return (table, keys, values)

    # keys = list(filter(lambda key: key not in exclude, vars(obj).keys()))
    # return (table, keys) 

def insert(obj, exclude: list[str]=['id']):
    import pdb;pdb.set_trace()
    table, keys, values = prepare_params(obj, None, exclude)
    valplaceholders = ('?,' * len(keys))[:-1]
    keys = ','.join(keys)
    query = f'insert into {table} ({keys}) values ({valplaceholders})'
    execute_query(query, values, f'inserting into {table}')
    
def update(obj, condition = 'id = ?', exclude: list[str] = []):
    table, keys, values = prepare_params(obj, condition, exclude)
    keys = [f'{key} = ?,' for key in keys]
    keys = ''.join(keys)
    query = f'update {table} set ({keys}) where {condition}'
    execute_query(query, values, f'updating table {table}')

def delete(obj, condition = 'id = ?', exclude: list[str] = []):
    table, keys, values = prepare_params(obj, condition, exclude)
    query = f'delete from {table} where {condition}'
    execute_query(query, values, f'deleting from table {table}')

def select(obj, select = '*', condition = 'id = ?', exclude: list[str] = []):
    table, keys, values = prepare_params(obj, condition, exclude)
    query = f'select {select} from {table} where {condition}'
    return execute_query(query, values, f'quering from {table}', 2)

def count(obj, select = '*', condition = 'id = ?'):
    table, keys, values = prepare_params(obj, condition)
    query = f'select count({select}) from {table} where {condition}'
    return execute_query(query, values, f'quering from {table}', 1)
