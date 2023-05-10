# first "users" commit comment
from flask import session, flash
import json
import base64
from typing import Dict, Any

from	webauthn	import	(
		generate_registration_options,
		verify_registration_response,
		generate_authentication_options,
		verify_authentication_response,
		options_to_json,
)
from webauthn.helpers import generate_challenge
from	webauthn.helpers.structs	import	(
		AuthenticatorSelectionCriteria,
		UserVerificationRequirement,
		RegistrationCredential,
		AuthenticationCredential,
)
from	webauthn.helpers.cose	import	COSEAlgorithmIdentifier

from flask_login import login_user, current_user
from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import chardet

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.models import EndUserWebAuthnCredential, _str_uuid
from sql_app.database import SessionLocal, engine

from mixpanel import Mixpanel
mp = Mixpanel("1ba15c80ce8bc4322c3cdbd7815f21e3")

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
	db = SessionLocal()
	try:
			yield db
	finally:
			db.close()



router = APIRouter(
	prefix="/users",
  tags=["users"],
)

# challenges
current_registration_challenge = None
current_authentication_challenge	=	None



# Default root endpoint
@router.get("/")
async def root():
  return { "message": "Hello world" }


# generate registration options
#
#
@router.get("/signup")
def generate_signup_options(domain: str, domain_name: str, email: str):
	
	global	current_registration_challenge
	
	options	=	generate_registration_options(
			rp_id=domain,
			rp_name=domain_name,
			user_id=_str_uuid(),
			user_name=email,
			
			authenticator_selection=AuthenticatorSelectionCriteria(
					user_verification=UserVerificationRequirement.REQUIRED),
			supported_pub_key_algs=[
					COSEAlgorithmIdentifier.ECDSA_SHA_256,
					COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
			],
	)
	
	current_registration_challenge	=	options.challenge
	
	return	options_to_json(options)#options_to_json(options)




# verify registration options
#
# recieve the request and parse
@router.post("/verify_signup")
def verify_signup_options(request: bytes, domain: str, origin: str, user: str, db: Session = Depends(get_db)):
	
	body = request
	
	credential = RegistrationCredential.parse_raw(body)

	verification	=	verify_registration_response(
			credential=credential,
			expected_challenge=current_registration_challenge,
			expected_rp_id=domain,
			expected_origin=origin,
	)
	
	print("if credential transports:")
	if credential.response.transports:
		print("credential:", credential.response.transports)
		print("credential type:", type(credential.response.transports))
		for transports in credential.response.transports:
			print(transports)
			print(type(transports))
			print("transports value:", transports.value)
			print("transports value type:", type(transports.value))
		# assign the value of the transport to be assigned to the user
		user_transport = transports.value
		user_transport_type = transports
		print("user transport: ", user_transport)
		print("user transport type: ", user_transport)

		
		# create new_user just like new_credential
		# add user to api database
		new_user = crud.get_end_user_by_email(db, email=user)
		# if user already exists with that email
		if new_user:
			raise HTTPException(status_code=400, detail="Email already registered")
		else:
			crud.create_end_user(db=db, user=user, org=origin)
			printed_eu = crud.get_end_user_by_email(db, email=user)
			print(printed_eu.id)
			# add new credential to current user
			crud.create_end_user_credential(db=db, credential= EndUserWebAuthnCredential(
					end_user_id = printed_eu.id,
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count,
					credential_transport = str(user_transport_type)
					
			))
			printed_eu = crud.get_end_user_by_email(db, email=user)
			print(printed_eu.org)
			print(printed_eu.credentials)
			# Note: you must supply the user_id who performed the event as the first parameter.
			mp.track("Verified Signup", 'End User Signup Verified',  {
				'Signup Verified': 'If Verified'
			})
			print("if statement verified")
			return	{"verified"	:	True}
			
	if not credential.response.transports :
		#	add	current	user to apoi database
		new_user = crud.get_end_user_by_email(db, email=user)
		
		# if user already exists with that email
		if new_user:
			raise HTTPException(status_code=400, detail="Email already registered")
		else:
			crud.create_end_user(db=db, user=user, org=origin)
		
			# add new credential to current user
			crud.create_end_user_credential(db=db, credential = EndUserWebAuthnCredential(
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count,
					
			))

			# print end user data
			printed_eu = crud.get_end_user_by_email(db, email=user)
			print(printed_eu.org)
			print(printed_eu.credentials)
			# Note: you must supply the user_id who performed the event as the first parameter.
			mp.track("Verified Signup", 'End User Signup Verified',  {
				'Signup Verified': 'Else Verified',
				'User' : origin
			})
			print("else statement verified")
			return	{"verified"	:	True}
		
	else:
		return	{"verified":	False,	"msg":	"error in api",	"status":	400}


# generate authentication options
#
#
@router.get("/login")
def generate_login_options(domain: str, email: str, db: Session = Depends(get_db)):
	print("IN	GENERATE	AUTH	OPTIONS")
	global	current_authentication_challenge
	
	
	# get user from email
	print("ASSIGNING	USER")
	user = crud.get_end_user_by_email(db=db, email=email)
	# user	=	User.query.filter_by(email=session['email']).first()
	# who is user?
	print(user.email)
	# what is users username?
	
	
	# get current user from session
	#user = User.query.filter_by(email=session['email']).first()
	# get the users
	print(f"USER.CREDENTIALS:	{user.credentials}")
	options	=	generate_authentication_options(
			rp_id=domain,
			# allow_credentials=[{
			# 		"type":	"public-key",
			# 		"id":	cred.credential_id,
			# 		"transports":	cred.credential_transport
			# }	for	cred	in	user.credentials],
			user_verification=UserVerificationRequirement.REQUIRED,
	)
	
	current_authentication_challenge	=	options.challenge
	
	return	options_to_json(options)


@router.post("/verify_login")
def verify_login_options(request: bytes, domain: str, origin: str, user: str, db: Session = Depends(get_db)):
	print("IN	verify	AUTH	OPTIONS")
	global	current_authentication_challenge
	
	body = request

	try:
			credential	=	AuthenticationCredential.parse_raw(body)

			#	Find	the	user's	corresponding	public	key
			
			user = crud.get_end_user_by_email(db=db, email=user)
			user_credential	=	None
			for	cred	in	user.credentials:
				print(cred)
				if	cred.credential_id	==	credential.raw_id:
						user_credential	=	cred

			if	user_credential	is	None:
				print("No cred found")
				raise	Exception("Could	not	find	corresponding	public	key	in	DB")

			#	Verify	the	assertion
			verification	=	verify_authentication_response(
					credential=credential,
					expected_challenge=current_authentication_challenge,
					expected_rp_id=domain,
					expected_origin=origin,
					credential_public_key=user_credential.credential_public_key,
					credential_current_sign_count=user_credential.current_sign_count,
					require_user_verification=True,
			)
	except	Exception	as	err:
			return	{"verified":	False,	"msg":	str(err),	"status":	400}

	#	Update	our	credential's	sign	count	to	what	the	authenticator	says	it	is	now
	user_credential.current_sign_count = verification.new_sign_count
	# log user in
	# Note: you must supply the user_id who performed the event as the first parameter.
	mp.track("Verified Login", 'End User Signup Verified',  {
		'Signup Verified': 'Else Verified',
		'User' : origin
	})
	return	{"verified":	True}