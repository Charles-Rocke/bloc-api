import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For sqlite below 
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# For postgres Testing DB below
SQLALCHEMY_DATABASE_URL = "postgresql://blocsquad_api_test_db:Zo9YZx9oY35yS6EcREYbEjiihXElZSTH@dpg-chvs0er3cv26tfmchsrg-a.ohio-postgres.render.com/bloc_api_testing_db_fc2n"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

# For postgres Production DB will go below
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency
def get_db():
	db = SessionLocal()
	try:
			yield db
	finally:
			db.close()