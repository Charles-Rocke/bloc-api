# first "users" commit comment
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
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models
from sql_app.models import User, WebAuthnCredential, _str_uuid
from sql_app.database import get_db
from mixpanel import Mixpanel

mp = Mixpanel("1ba15c80ce8bc4322c3cdbd7815f21e3")



router = APIRouter(
	prefix="/bloc/users",
  tags=["bloc users"],
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
@router.get("/signup")
def generate_signup_options(domain: str, domain_name: str, email: str, db: Session = Depends(get_db)):
	# send request to endpoint to generate options
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
	
	return	options_to_json(options)




# verify registration options
#
# recieve the request and parse
@router.post("/verify_signup")
def verify_signup_options(request: bytes, domain: str, domain_origin: str, email: str, pricing_plan: str, user_api_key: str, user_timezone: str,db: Session = Depends(get_db)):
	
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
		new_user = crud.get_user_by_email(db, email=email)

		# if user already exists with that email
		if new_user:
			raise HTTPException(status_code=400, detail="Email already registered")
		else:
			print(f"pricing plan: {pricing_plan}")
			crud.create_user(db=db, email=email, pricing_plan=pricing_plan, api_key=user_api_key, timezone=user_timezone)

			# add new credential to current user
			crud.create_user_credential(db=db, credential= WebAuthnCredential(
					user_email = email,
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count,
					credential_transport = str(user_transport_type)
					
			))
			# Note: you must supply the user_id who performed the event as the first parameter.
			new_added_user = crud.get_user_by_email(db, email=email)
			mp.track(new_added_user.id, 'User API Signup Request',  {
				'Request': 'Signed up with Transports',
				'User Username' : new_added_user.email,
				'Pricing plan' : pricing_plan,
			})
			return	{"verified"	:	True}
	if not credential.response.transports :
		#	add	current	user to apoi database
		new_user = crud.get_user_by_email(db, email=email)
		
		# if user already exists with that email
		if new_user:
			raise HTTPException(status_code=400, detail="Email already registered")
		else:
			crud.create_user(db=db, email=email, pricing_plan=pricing_plan, api_key=user_api_key, timezone=user_timezone)
		
			# add new credential to current user
			crud.create_user_credential(db=db, credential = WebAuthnCredential(
					user_email = email,
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count,
					
			))

			# Note: you must supply the user_id who performed the event as the first parameter.
			new_added_user = crud.get_user_by_email(db, email=email)
			mp.track(new_added_user.id, 'User API Signup Request',  {
				'Request': 'Signed up with no Transports',
				'End User Username' : new_added_user.email,
				'Pricing plan' : pricing_plan,
			})
			return	{"verified"	:	True}
		
	else:
		return	{"verified":	False,	"msg":	"error in api",	"status":	400}


# generate authentication options
#
#
@router.get("/login")
def generate_login_options(domain: str, email: str, db: Session = Depends(get_db)):
	global	current_authentication_challenge
	
	options	=	generate_authentication_options(
			rp_id=domain,
			user_verification=UserVerificationRequirement.REQUIRED,
	)
	
	current_authentication_challenge	=	options.challenge
	
	return	options_to_json(options)


@router.post("/verify_login")
def verify_login_options(request: bytes, domain: str, domain_origin: str, email: str, db: Session = Depends(get_db)):
	global	current_authentication_challenge
	
	body = request

	try:
			credential	=	AuthenticationCredential.parse_raw(body)
			#	Find	the	user's	corresponding	public	key
			user = crud.get_user_by_email(db=db, email=email)
			user_credential	=	None
			for	cred	in	user.credentials:
					if	cred.credential_id	==	credential.raw_id:
							user_credential	=	cred

			if	user_credential	is	None:
					raise	Exception("Could	not	find	corresponding	public	key	in	DB")

			#	Verify	the	assertion
			verification	=	verify_authentication_response(
					credential=credential,
					expected_challenge=current_authentication_challenge,
					expected_rp_id=domain,
					expected_origin=domain_origin,
					credential_public_key=user_credential.credential_public_key,
					credential_current_sign_count=user_credential.current_sign_count,
					require_user_verification=True,
			)
	except	Exception	as	err:
			return	{"verified":	False,	"msg":	str(err),	"status":	400}

	#	Update	our	credential's	sign	count	to	what	the	authenticator	says	it	is	now
	user_credential.current_sign_count = verification.new_sign_count
	# log user in
	mp.track(user.id, 'User API Login Request',  {
		'Request': 'Verified',
		'User Username': user.email,
	})
	return	{"verified":	True}