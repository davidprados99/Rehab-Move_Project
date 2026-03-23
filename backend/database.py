import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#Database.py is responsible for setting up the connection to the PostgreSQL database using SQLAlchemy. It defines the database URL, creates the engine, and provides a function to get a database session.

load_dotenv()

# Build the database URL from environment variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

#sqlalchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#SessionLocal class will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for our models
Base = declarative_base()

# Function to get a database session, we will use this in our API endpoints to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

