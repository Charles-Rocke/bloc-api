import uvicorn
from bloc.app import create_app
from resources import users

app = create_app()
app.include_router(users.router)

if	__name__	==	"__main__":
		#	run	flask	application
		uvicorn.run(app, host="0.0.0.0", port=8000)