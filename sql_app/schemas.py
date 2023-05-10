from pydantic import BaseModel

# credential schema
class CredentialBase(BaseModel):
    title: str
    description: str | None = None


class CredentialCreate(CredentialBase):
	user_email: str
	credential_id: bytes
	credential_public_key: bytes
	current_sign_count: int


class Credential(CredentialBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# User schema
class UserBase(BaseModel):
    email: str



class User(UserBase):
    id: int
    credentials: list[Credential] = []

    class Config:
        orm_mode = True