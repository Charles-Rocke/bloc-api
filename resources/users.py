# first "users" commit comment
from flask import request, session, flash
import json
import base64

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

from bloc.app import db
from models.models import User, WebAuthnCredential, _str_uuid
from flask_login import login_user, current_user
from pydantic import BaseModel
from fastapi import APIRouter
import chardet
router = APIRouter(
	prefix="/users",
  tags=["users"],
)

current_registration_challenge = None

# Schema
class Payload(BaseModel):
	key: str


# Default root endpoint
@router.get("/")
async def root():
  return { "message": "Hello world" }


# generate registration options
@router.get("/signup")
def generate_signup_options(domain: str, domain_name: str, user_uid: str, email: str):
	# send request to endpoint to generate options
	print("IN	GENERATE	REG	OPTIONS")
	global	current_registration_challenge
	

	
	# new_user	=	User(uid=session["user_uid"], email=session["email"])
	# session["new_user"] = new_user
	# print(session["new_user"])
	# print(type(session["new_user"]))
	'''
 	options	=	generate_registration_options(
		rp_id=rp_id,
		rp_name=rp_name,
		user_id=user.uid,
		user_name=user.email,
		exclude_credentials=[{
				"id":	cred.id,
				"transports":	cred.transports,
				"type":	"public-key"
		}	for	cred	in	user.credentials],
		authenticator_selection=AuthenticatorSelectionCriteria(
				user_verification=UserVerificationRequirement.REQUIRED),
		supported_pub_key_algs=[
				COSEAlgorithmIdentifier.ECDSA_SHA_256,
				COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
		],
	)
	'''
	options	=	generate_registration_options(
			rp_id=domain,
			rp_name=domain_name,
			user_id=user_uid,
			user_name=email,
			
			authenticator_selection=AuthenticatorSelectionCriteria(
					user_verification=UserVerificationRequirement.REQUIRED),
			supported_pub_key_algs=[
					COSEAlgorithmIdentifier.ECDSA_SHA_256,
					COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
			],
	)
	
	current_registration_challenge	=	options.challenge
	print(type(options))
	print(options.challenge)
	print()
	print()
	decoded = base64.b64decode(options.challenge)
	print(decoded)
	print()
	print(f'options_to_json(options): {options_to_json(options)}')
	print(f'type options_to_json(options): {type(options_to_json(options))}')
	json_object = json.loads(options_to_json(options))
	print()
	print(json_object)
	print(type(json_object))
	json.dumps(json_object)
	print()
	print()
	options.challenge = decoded
	print(options.challenge)
	print(options_to_json(options))
	return	options_to_json(options)#options_to_json(options)


	# NEED TO FIND A WAY TO SEND BINARY DATA FOR USER TO USE BINARY CHALLENGE FOR VERIFICATION





	
	# print("IN	GENERATE	REG	OPTIONS")
	# global current_registration_challenge
	

	
	# # new_user	=	User(uid=session["user_uid"], email=session["email"])
	# # session["new_user"] = new_user
	# # print(session["new_user"])
	# # print(type(session["new_user"]))
	# '''
	# options	=	generate_registration_options(
	# 	rp_id=rp_id,
	# 	rp_name=rp_name,
	# 	user_id=user.uid,
	# 	user_name=user.email,
	# 	exclude_credentials=[{
	# 			"id":	cred.id,
	# 			"transports":	cred.transports,
	# 			"type":	"public-key"
	# 	}	for	cred	in	user.credentials],
	# 	authenticator_selection=AuthenticatorSelectionCriteria(
	# 			user_verification=UserVerificationRequirement.REQUIRED),
	# 	supported_pub_key_algs=[
	# 			COSEAlgorithmIdentifier.ECDSA_SHA_256,
	# 			COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
	# 	],
	# )
	# '''
	# options	=	generate_registration_options(
	# 		rp_id=domain,
	# 		rp_name=domain_name,
	# 		user_id=user_uid,
	# 		user_name=email,
			
			
	# 		authenticator_selection=AuthenticatorSelectionCriteria(
	# 				user_verification=UserVerificationRequirement.REQUIRED),
	# 		supported_pub_key_algs=[
	# 				COSEAlgorithmIdentifier.ECDSA_SHA_256,
	# 				COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
	# 		],
	# )
	# #print(options.challenge)
	# opts_challenge = options.challenge
	# opts = options_to_json(options)
	# print(f'options_to_json(options): {options_to_json(options)}')
	# print(f'type options_to_json(options): {type(options_to_json(options))}')
	# options_object = json.loads(options_to_json(options))
	# options_object["challenge"] = opts_challenge
	# opts_obj = pickle.dumps(options_object)
	# # print(options_object)
	# # print(type(str(options_object)))
	# # print(str(options_object))
	# # print("dumping")
	# # opts_obj_to_json = json.dumps(str(options_object))
	# # print("finished dumping")
	# #print(opts_obj_to_json)
	# return	pickle.loads(opts_obj)