from google.appengine.ext import db

class Citizen(db.Model):
	citizen_name = db.StringProperty(required = True)
	citizen_id = db.IntegerProperty(required = True)
	citizen_mu_id = db.IntegerProperty(required = True)

class MilitaryUnit(db.Model):
	mu_name = db.StringProperty(required = True)
	mu_id = db.IntegerProperty(required = True)
	mu_location = db.StringProperty(required = True)
	mu_members_count = db.IntegerProperty(required = True)

class CitizenData(db.Model):
	citizen_id = db.IntegerProperty(required = True)
	citizen_mu_id = db.IntegerProperty(required = True)
	date = db.DateProperty(required = True)
	rank = db.IntegerProperty(required = True)

class MUDamage(db.Model):
	mu_id = db.IntegerProperty(required = True)
	date = db.DateProperty(required = True)
	damage = db.IntegerProperty(required = True)