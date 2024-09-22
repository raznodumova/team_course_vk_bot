from sqlalchemy import create_engine
import psycopg2
from sqlalchemy.orm import Session, sessionmaker

def check_conn():
    engine = create_engine(f"postgresql://postgres:admin@localhost:5432/vk_bots", echo=True)
    engine.connect()
    return engine


session = sessionmaker(bind=check_conn())