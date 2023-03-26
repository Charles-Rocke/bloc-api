# first "users" commit comment
from flask import request, session, flash
import json

from	webauthn	import	(
		generate_registration_options,
		verify_registration_response,
		generate_authentication_options,
		verify_authentication_response,
		options_to_json,
)
from	webauthn.helpers.structs	import	(
		AuthenticatorSelectionCriteria,
		UserVerificationRequirement,
		RegistrationCredential,
		AuthenticationCredential,
)
from	webauthn.helpers.cose	import	COSEAlgorithmIdentifier

from bloc.app import db
from models.models import User, WebAuthnCredential, _str_uuid
from flask_login import login_user, current_user
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(
	prefix="/users",
  tags=["users"],
)
# Schema
class Payload(BaseModel):
	key: str


# Default root endpoint
@router.get("/")
async def root():
  return { "message": "Hello world" }

