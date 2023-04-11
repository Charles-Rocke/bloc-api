from bloc.app import db
from flask_login import UserMixin
from sqlalchemy.orm import backref
import uuid


def _str_uuid():
    return str(uuid.uuid4())


class Form(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# logo (tbd)
	# header
	header = db.Column(db.String, nullable = True)
	# fieldName
	field_name = db.Column(db.String, nullable = True)
	# primaryColor
	primary_color = db.Column(db.String, nullable = True)
	# secondaryColor
	secondary_color = db.Column(db.String, nullable = True)
	# companyName
	company_name = db.Column(db.String, nullable = True)
	# related table
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



# Users
class User(db.Model, UserMixin):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	# user unique id/API key
	uid = db.Column(db.String(40), default= _str_uuid, unique=True)
	# users email
	email = db.Column(db.String(150), unique = True)
	# users form
	forms = db.relationship('Form')
	credentials = db.relationship(
		"WebAuthnCredential",
		backref=backref("user", cascade="all, delete"),
		lazy=True,
  )
	end_users = db.relationship("EndUser", backref=backref("user", cascade="all, delete"), lazy=True,)
	

# WebAuthnCredentials
class WebAuthnCredential(db.Model):
	"""Stored WebAuthn Credentials as a replacement for passwords."""
	__tablename__ = "credential"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	end_user_id = db.Column(db.Integer, db.ForeignKey("enduser.id"))
	credential_id = db.Column(db.LargeBinary, nullable=False)
	credential_public_key = db.Column(db.LargeBinary, nullable=False)
	current_sign_count = db.Column(db.Integer, default=0)
	# some devices dont generate transports
	credential_transport = db.Column(db.String, nullable = True)

	def __repr__(self):
			return f"<Credential {self.credential_id}>"


# end user
class EndUser(db.Model):
	__tablename__ = "enduser"

	id = db.Column(db.Integer, primary_key=True)
	# end users username
	username = db.Column(db.String())
	# end users organization of origin
	org = db.Column(db.Integer, db.ForeignKey("user.id"))
	# end users optional webauthn credential
	credentials = db.relationship(
		"WebAuthnCredential",
		backref=backref("enduser", cascade="all, delete"),
		lazy=True,
  )