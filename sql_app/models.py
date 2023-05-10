from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship, backref
import uuid
from sql_app.database import Base


def _str_uuid():
    return str(uuid.uuid4())


class Form(Base):
	
	__tablename__ = "forms"
	
	id = Column(Integer, primary_key=True)
	# logo (tbd)
	# header
	header = Column(String, nullable = True)
	# fieldName
	field_name = Column(String, nullable = True)
	# primaryColor
	primary_color = Column(String, nullable = True)
	# secondaryColor
	secondary_color = Column(String, nullable = True)
	# companyName
	company_name = Column(String, nullable = True)
	# related table
	user_email = Column(Integer, ForeignKey('users.email'))



# Users
class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	# user unique id/API key
	uid = Column(String(40), default= _str_uuid, unique=True)
	# users email
	email = Column(String(150), unique = True)
	# users form
	forms = relationship('Form')
	credentials = relationship(
		"WebAuthnCredential",
		backref=backref("users", cascade="all, delete"),
		lazy=True,
  )
	end_users = relationship("EndUser", backref=backref("users", cascade="all, delete"), lazy=True,)
	

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
