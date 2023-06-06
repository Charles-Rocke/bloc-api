from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship, backref
import uuid
from sqlalchemy.ext.declarative import declarative_base
import math

Base = declarative_base()

def _str_uuid():
    return str(uuid.uuid4())



# Users
class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	# user unique id/API key
	uid = Column(String(40), default= _str_uuid, unique=True)
	# user api key
	api_key = Column(String(), unique=True)
	# users email
	email = Column(String(150), unique = True)
	# users form
	end_users = relationship("EndUser", backref=backref("users", cascade="all, delete"), lazy=True,)
	credentials = relationship(
		"WebAuthnCredential",
		backref=backref("user", cascade="all, delete"),
		lazy=True,
  )
	# pricing plan
	pricing_plan = Column(String(10))
	# total logins for pricing plan
	login_count = Column(Integer)
	

# WebAuthnCredentials
class WebAuthnCredential(Base):
	"""Stored WebAuthn Credentials as a replacement for passwords."""
	
	__tablename__ = "credentials"
	
	id = Column(Integer, primary_key=True)
	user_email = Column(Integer, ForeignKey("users.email"), nullable=False)
	credential_id = Column(LargeBinary, nullable=False)
	credential_public_key = Column(LargeBinary, nullable=False)
	current_sign_count = Column(Integer, default=0)
	# some devices dont generate transports
	credential_transport = Column(String, nullable = True)

	def __repr__(self):
			return f"<Credential {self.credential_id}>"


# end user
class EndUser(Base):
	
	__tablename__ = "endusers"

	id = Column(Integer, primary_key=True)
	# end users username
	email = Column(String())
	# end users organization of origin
	org = Column(Integer, ForeignKey("users.id"))
	# end users optional webauthn credential
	credentials = relationship(
		"EndUserWebAuthnCredential",
		backref=backref("endusers", cascade="all, delete"),
		lazy=True,
  )


# End User WebAuthnCredentials
class EndUserWebAuthnCredential(Base):
	"""Stored WebAuthn Credentials as a replacement for passwords."""
	
	__tablename__ = "endusercredentials"
	
	id = Column(Integer, primary_key=True)
	end_user_id = Column(Integer, ForeignKey("endusers.id"))
	credential_id = Column(LargeBinary, nullable=False)
	credential_public_key = Column(LargeBinary, nullable=False)
	current_sign_count = Column(Integer, default=0)
	# some devices dont generate transports
	credential_transport = Column(String, nullable = True)

	def __repr__(self):
			return f"<Credential {self.credential_id}>"