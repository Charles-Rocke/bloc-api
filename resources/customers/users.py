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
from sql_app.models import EndUserWebAuthnCredential, _str_uuid, User
from sql_app.database import get_db
# analytics 
from mixpanel import Mixpanel
mp = Mixpanel("1ba15c80ce8bc4322c3cdbd7815f21e3")





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
  return { "message": "Hello from bloc" }


# generate registration options
#
#
# start end user sign up
@router.get("/signup")
def generate_signup_options(api_key: str, domain: str, domain_name: str, user_email: str, db: Session = Depends(get_db)):

	# api key check
	user = crud.get_user_by_api_key(db, api_key)
	if user:
		global	current_registration_challenge
		
		options	=	generate_registration_options(
				rp_id=domain,
				rp_name=domain_name,
				user_id=_str_uuid(),
				user_name=user_email,
				
				authenticator_selection=AuthenticatorSelectionCriteria(
						user_verification=UserVerificationRequirement.REQUIRED),
				supported_pub_key_algs=[
						COSEAlgorithmIdentifier.ECDSA_SHA_256,
						COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
				],
		)
		
		current_registration_challenge	=	options.challenge
		
		return	options_to_json(options)#options_to_json(options)
	else:
		return {"API Key Error message" : "No user found with that api_key"}




# verify registration options
#
#
# verify end user sign up
@router.post("/verify_signup")
def verify_signup_options(api_key: str, request: bytes, domain: str, domain_origin: str, user_email: str, db: Session = Depends(get_db)):

	# api key check
	user = crud.get_user_by_api_key(db, api_key)
	if user:
		body = request
		
		credential = RegistrationCredential.parse_raw(body)
	
		verification	=	verify_registration_response(
				credential=credential,
				expected_challenge=current_registration_challenge,
				expected_rp_id=domain,
				expected_origin=domain_origin,
		)
		
		if credential.response.transports:
			for transports in credential.response.transports:
				pass
			# assign the value of the transport to be assigned to the user
			user_transport_type = transports
	
			
			# create new_user just like new_credential
			# add user to api database
			new_user = crud.get_end_user_by_email(db, email=user_email)
			# if user already exists with that email
			if new_user:
				raise HTTPException(status_code=400, detail="Email already registered")
			else:
				crud.create_end_user(db=db, user=user_email, org=domain_origin)
				printed_eu = crud.get_end_user_by_email(db, email=user_email)
				print(printed_eu.id)
				# add new credential to current user
				crud.create_end_user_credential(db=db, credential= EndUserWebAuthnCredential(
						end_user_id = printed_eu.id,
						credential_id=verification.credential_id,
						credential_public_key=verification.credential_public_key,
						current_sign_count=verification.sign_count,
						credential_transport = str(user_transport_type)
						
				))
	
				# Note: you must supply the user_id who performed the event as the first parameter.
				new_added_end_user = crud.get_end_user_by_email(db, email=user_email)
				mp.track(new_added_end_user.id, 'End User API Signup Request',  {
					'Request': 'If Verified',
					'End User Username' : new_added_end_user.email,
					'From User' : domain_origin
				})
				
				# add parent user login count by on below
				user = crud.get_user_by_api_key(db, api_key=api_key)
				# check other pricing plans first
				if user.pricing_plan != "starter":
					user.login_count += 1
				# check if User reached 20 logins and is on the starter plan
				elif user.pricing_plan == "starter" and user.login_count < 20:
					# increase the login count
					user.login_count += 1
				else:
					return {"verified" : False,
									"message" : "Reached max logins for this month. Upgrade plans to get unlimited logins"
								 }
				# end login count
				return	{"verified"	:	True}
				
		if not credential.response.transports :
			#	add	current	user to apoi database
			new_user = crud.get_end_user_by_email(db, email=user_email)
			
			# if user already exists with that email
			if new_user:
				raise HTTPException(status_code=400, detail="Email already registered")
			else:
				crud.create_end_user(db=db, user=user_email, org=domain_origin)
			
				# add new credential to current user
				crud.create_end_user_credential(db=db, credential = EndUserWebAuthnCredential(
						credential_id=verification.credential_id,
						credential_public_key=verification.credential_public_key,
						current_sign_count=verification.sign_count,
						
				))
				# Note: you must supply the user_id who performed the event as the first parameter.
				new_added_end_user = crud.get_end_user_by_email(db, email=user_email)
				mp.track(new_added_end_user.id, 'End User API Signup Request',  {
					'Request': 'Else Verified',
					'End User Username' : new_added_end_user.email,
					'From User' : domain_origin
				})
				# add parent user login count by on below
				user = crud.get_user_by_api_key(db, api_key=api_key)
				# check other pricing plans first
				if user.pricing_plan != "starter":
					user.login_count += 1
				# check if User reached 20 logins and is on the starter plan
				elif user.pricing_plan == "starter" and user.login_count < 20:
					# increase the login count
					user.login_count += 1
				else:
					return {"verified" : False,
									"message" : "Reached max logins for this month. Upgrade plans to get unlimited logins"
								 }
				# end login count
				return	{"verified"	:	True}
			
		else:
			return	{"verified":	False,	"msg":	"error in api",	"status":	400}
	else:
		return {"API Key Error message" : "No user found with that api_key"}



# generate authentication options
#
#
# start end user login
@router.get("/login")
def generate_login_options(api_key: str, domain: str, user_email: str, db: Session = Depends(get_db)):
	# api key check
	user = crud.get_user_by_api_key(db, api_key)
	if user:
		global	current_authentication_challenge
		
		options	=	generate_authentication_options(
				rp_id=domain,
				user_verification=UserVerificationRequirement.REQUIRED,
		)
		
		current_authentication_challenge	=	options.challenge
		
		return	options_to_json(options)
	else:
		return {"API Key Error message" : "No user found with that api_key"}


# verify end user login
@router.post("/verify_login")
def verify_login_options(api_key: str, request: bytes, domain: str, domain_origin: str, user_email: str, db: Session = Depends(get_db)):
	# api key check
	user = crud.get_user_by_api_key(db, api_key)
	if user:
		print("print me")
		global	current_authentication_challenge
		
		body = request
	
		try:
			print("in try")
			print("credential")
			credential	=	AuthenticationCredential.parse_raw(body)
	
			#	Find	the	user's	corresponding	public	key
			print("end_user")
			end_user = crud.get_end_user_by_email(db=db, email=user_email)
			print("end_user_credential")
			end_user_credential	=	None
			print("for loop")
			for	cred	in	end_user.credentials:
				print("if statement")
				if	cred.credential_id	==	credential.raw_id:
					print("end_user_credential = cred")
					end_user_credential	=	cred
	
			if	end_user_credential	is	None:
				raise	Exception("Could	not	find	corresponding	public	key	in	DB")
	
			#	Verify	the	assertion
			print("verification_auth_response")
			verification	=	verify_authentication_response(
					credential=credential,
					expected_challenge=current_authentication_challenge,
					expected_rp_id=domain,
					expected_origin=domain_origin,
					credential_public_key=end_user_credential.credential_public_key,
					credential_current_sign_count=end_user_credential.current_sign_count,
					require_user_verification=True,
			)
		except	Exception	as	err:
				return	{"verified":	False,	"msg":	str(err),	"status":	400}
	
		#	Update	our	credential's	sign	count	to	what	the	authenticator	says	it	is	now
		print("sign_count")
		end_user_credential.current_sign_count = verification.new_sign_count
	
		# Note: you must supply the user_id who performed the event as the first parameter.
		print("mixpanel")
		mp.track(end_user.id, 'End User API Login Request',  {
			'Request': 'Verified',
			'End User Username': end_user.email,
			'From User': domain_origin
		})
		
		# add parent user login count by on below
		user = crud.get_user_by_api_key(db, api_key=api_key)
		# check other pricing plans first
		if user.pricing_plan != "starter":
			user.login_count += 1
		# check if User reached 20 logins and is on the starter plan
		elif user.pricing_plan == "starter" and user.login_count < 20:
			# increase the login count
			user.login_count += 1
		else:
			return {"verified" : False,
							"message" : "Reached max logins for this month. Upgrade plans to get unlimited logins"
						 }
		# end login count
		return	{"verified":	True}
	else:
		return {"API Key Error message" : "No user found with that api_key"}