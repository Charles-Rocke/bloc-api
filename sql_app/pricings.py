import math

# class Plans
class Plans():
	# attributes
	def __init__(self, type, price, max_logins):
		# type
		self.type = type
		# price
		self.price = price
		# num logins
		self.max_logins = max_logins

# methods
	# get type
	def get_type(self):
		return self.type
	
	# get price
	def get_price(self):
		return self.price
	
	# get num logins
	def get_max_logins(self):
		return self.max_logins
	
	# set type
	def set_type(self, t):
		self.type = t
	
	# set price
	def set_price(self):
		if self.type == "enterprise":
			self.price = 0.10
		elif self.type == "growth":
			self.price = 0.15
		else:
			self.price = 0.00

	# set max logins
	def set_max_logins(self):
		if self.type == "starter":
			self.max_logins = 20
		else:
			self.max_logins = math.inf