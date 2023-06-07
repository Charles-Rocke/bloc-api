# read data
from sqlalchemy.orm import Session

from . import models, schemas

"""
	These are User crud methods
"""
# bloc users
# get bloc user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# get bloc user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# get bloc user by api key
def get_user_by_api_key(db: Session, api_key: str):
	return db.query(models.User).filter(models.User.api_key == api_key).first()

# get all bloc users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# create bloc user
def create_user(db: Session, email: str, pricing_plan: str, api_key: str, timezone: str):
    db_user = models.User(email=email, pricing_plan=pricing_plan, api_key=api_key, timezone=timezone, login_count=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# get bloc user credentials
def get_credentials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WebAuthnCredential).offset(skip).limit(limit).all()

# get bloc user credential
def create_user_credential(db: Session, credential: models.WebAuthnCredential):
    db_credential = credential
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


"""
	These are End user crud methods
"""
# bloc users end users
# get end user by id
def get_end_user(db: Session, user_id: int):
    return db.query(models.EndUser).filter(models.EndUser.id == user_id).first()

# get end user by email
def get_end_user_by_email(db: Session, email: str):
    return db.query(models.EndUser).filter(models.EndUser.email == email).first()

# get all end users
def get_end_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EndUser).offset(skip).limit(limit).all()

# create end user
def create_end_user(db: Session, user: str, origin: str, parent_org_id: int):
    db_end_user = models.EndUser(email=user, origin=origin, parent_org = parent_org_id)
    db.add(db_end_user)
    db.commit()
    db.refresh(db_end_user)
    return db_end_user

# get end user credentials
def get_end_user_credentials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EndUserWebAuthnCredential).offset(skip).limit(limit).all()

# create end user credentials
def create_end_user_credential(db: Session, credential: models.EndUserWebAuthnCredential):
    db_credential = credential
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential