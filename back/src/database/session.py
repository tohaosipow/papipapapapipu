from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, encoding='utf-8',
					   pool_size=50, max_overflow=-1)

db_session = scoped_session(
	sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
