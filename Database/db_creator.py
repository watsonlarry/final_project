from config import config
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

# useful info for psycopg2:
# https://stackoverflow.com/questions/34484066/create-a-postgres-database-using-python


class MyDB(object):
    def __init__(self):
        self.params = config()

    def create_new_db(self, newdb):
        user, host, port = self.params['user'], self.params['host'], self.params['port']
        pw = self.params['password']
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, pw, host, port, newdb)

        self.engine = create_engine(url, client_encoding='utf8')
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        # print(database_exists(engine.url))

def df2postgres(engine, df):
    con = engine.connect()
    df.to_sql(name='records', con=con, if_exists='replace', index=True, chunksize=10)

    return con


# Have Database store static data for use during the project
if __name__ == '__main__':

    homeless_db = MyDB()
    homeless_db.create_new_db('homeless_db')
    engn = homeless_db.engine
    education_df = pd.read_csv('../Machine Learning/Resources/processed_education.csv', delimiter=',', encoding='utf-8')
    homeless_df = pd.read_csv('../Machine Learning/Resources/processed_homeless.csv', delimiter=',', encoding='utf-8')
    con = df2postgres(engine=engn, df=education_df)
    con = df2postgres(engine=engn, df=homeless_df)
    dta = con.execute('SELECT * FROM records LIMIT 5;')
    print(dta.fetchall())