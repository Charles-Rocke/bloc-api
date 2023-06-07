from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from main import app
from sqlalchemy.orm import Session
from database import get_db
from sql_app.models import User
from datetime import datetime


scheduler = BackgroundScheduler()

def reset_login_counts(db: Session):
	# Retrieve users from the database
	users = db.query(User).all()

	# Iterate through the users and reset login counts based on their timezones and the current day
	for user in users:
		# Get the current date and time in the user's timezone
		user_timezone = user.timezone  # Replace with the actual attribute that stores the user's timezone
		user_current_date = datetime.now(tz=user_timezone).date()

		# Check if it's the first day of the month for the user
		if user_current_date.day == 1:
			user.login_count = 0

	# Commit the changes to the database
	db.commit()

# Configure the task to run at midnight on the first day of every month in the user's timezone
@app.on_event("startup")
def schedule_login_count_reset():
	with app.container as container:
		db = next(get_db())

		users = db.query(User).all()

		for user in users:
			scheduler.add_job(
				reset_login_counts,
				args=[db],
				trigger=CronTrigger(day=1, hour=0, minute=0, second=0),
				timezone=user.timezone
			)

# Start the scheduler
scheduler.start()

# Ensure the scheduler shuts down gracefully when the app exits
@app.on_event("shutdown")
def shutdown_event():
  scheduler.shutdown()