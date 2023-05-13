# read data
from sqlalchemy.orm import Session

from . import models, schemas

# bloc users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: str):
    db_user = models.User(email=user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# create
def get_credentials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WebAuthnCredential).offset(skip).limit(limit).all()


def create_user_credential(db: Session, credential: models.WebAuthnCredential):
    db_credential = credential
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


# users end users
# read data

def get_end_user(db: Session, user_id: int):
    return db.query(models.EndUser).filter(models.EndUser.id == user_id).first()


def get_end_user_by_email(db: Session, email: str):
    return db.query(models.EndUser).filter(models.EndUser.email == email).first()


def get_end_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EndUser).offset(skip).limit(limit).all()


def create_end_user(db: Session, user: str, org: str):
    db_end_user = models.EndUser(email=user, org=org)
    db.add(db_end_user)
    db.commit()
    db.refresh(db_end_user)
    return db_end_user


# create
def get_end_user_credentials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EndUserWebAuthnCredential).offset(skip).limit(limit).all()


def create_end_user_credential(db: Session, credential: models.EndUserWebAuthnCredential):
    db_credential = credential
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential