import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For sqlite below 
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# For postgres Testing DB below
# SQLALCHEMY_DATABASE_URL = "postgresql://blocsquad_api_test_db:eZBhN2vVO9lxtjf6LsFav5EzIt4PmvTh@dpg-ci0ame3hp8ue00dkdjn0-a.ohio-postgres.render.com/bloc_api_test_db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_pre_ping=True,
# )

# For postgres Production DB will go below
SQLALCHEMY_DATABASE_URL = "postgresql://blocsquad_api_prod_db:1ilC1uCGyv2GSKFib3nA4AjszT8C0MBU@dpg-ci1mg6g2qv2fv4rvj8qg-a.ohio-postgres.render.com/bloc_api_prod_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency
def get_db():
	db = SessionLocal()
	try:
			yield db
	finally:
			db.close()