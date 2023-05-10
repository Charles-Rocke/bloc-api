import uvicorn
from bloc.app import create_app
from resources.bloc import users as bloc_users
from resources.customers import users as customers_users

app = create_app()
app.include_router(bloc_users.router)
app.include_router(customers_users.router)

if	__name__	==	"__main__":
		#	run	flask	application
		uvicorn.run(app, host="0.0.0.0", port=8000)