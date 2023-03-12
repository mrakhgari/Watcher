from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database_api.configs  as configs


engine = create_engine(configs.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

session_local = sessionmaker(bind=engine, autoflush=False)



def get_db():
    '''
        get session object. 
    '''
    session = session_local()
    try:
        yield session 
    except:
        session.close()

