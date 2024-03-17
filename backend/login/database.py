import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 



class Credentials:
  def __init__(self, database, user, password, host, post):
    self.database = database
    self.user = user
    self.password = password
    self.host = host
    self.post = post



def create_database():
    con = psycopg2.connect(dbname='postgres',
        user=self.user_name, host='',
        password=self.password)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

    cur = con.cursor()

    # Use the psycopg2.sql module instead of string concatenation 
    # in order to avoid sql injection attacks.
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(self.db_name))
        )


def create_table(credentials):
    conn = psycopg2.connect(database = credentials.database, user = credentials.user, password = credentials.password, host = credentials.host, port = credentials.post)
    print "Opened database successfully"

    cur = conn.cursor()
    cur.execute('''CREATE TABLE COMPANY
        (ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        AGE            INT     NOT NULL,
        ADDRESS        CHAR(50),
        SALARY         REAL);''')
    print "Table created successfully"

    conn.commit()
    conn.close()


def insert_vendor(vendor_name):
    """ Insert a new vendor into the vendors table """

    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    
    vendor_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (vendor_name,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    vendor_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return vendor_id


def insert_many_vendors(vendor_list):
    """ Insert multiple vendors into the vendors table  """

    sql = "INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING *"
    config = load_config()
    rows = []

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, vendor_list)

                # obtain the inserted rows
                rows = cur.fetchall()

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return rows