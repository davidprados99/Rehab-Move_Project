import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#Database.py is responsible for setting up the connection to the PostgreSQL database using SQLAlchemy. It defines the database URL, creates the engine, and provides a function to get a database session.

load_dotenv()

# Get context variables for database connection
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# If some variables are missing, we fall back to SQLite for testing purposes

if not DB_USER or not DB_PASSWORD or not DB_HOST or not DB_NAME:
    print("Configuración DB no encontrada. Usando SQLite para tests")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    # Check same thread is needed for SQLite to avoid issues with multiple threads accessing the database
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # If all variables are present, we connect to PostgreSQL
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Conectado a PostgreSQL: {DB_NAME}")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()