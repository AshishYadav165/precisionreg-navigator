from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class FDAPrecedent(Base):
    __tablename__ = "fda_precedents"

    id = Column(Integer, primary_key=True)
    trade_name = Column(String)
    sponsor = Column(String)
    disease_use = Column(String)
    biomarker = Column(String)
    platform = Column(String)
    specimen_type = Column(String)
    route = Column(String)
    submission_number = Column(String)
    cdx_flag = Column(Boolean)
    summary_url = Column(String)

def get_engine(sqlite_path: str):
    return create_engine(f"sqlite:///{sqlite_path}")

def init_db(sqlite_path: str):
    engine = get_engine(sqlite_path)
    Base.metadata.create_all(engine)
    return engine

def get_session(sqlite_path: str):
    engine = get_engine(sqlite_path)
    Session = sessionmaker(bind=engine)
    return Session()
