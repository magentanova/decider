from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Decider.secrets import db_password

user = 'justinrichards'
host = 'deciderdb-instance.cueeuh8xzl8r.us-east-2.rds.amazonaws.com'
port = 5432
conn_string = 'postgresql://{user}:{pw}@{host}:{port}/deciderdb'.format(
    host=host,
    pw=db_password,
    port=port,
    user=user
)

engine = create_engine(conn_string)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
