from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('foods.sqlite')

class Farmer(UserMixin, Model):
  name=CharField()
  username=CharField(unique=True)
  password=CharField()

  class Meta:
    database = DATABASE


class Food(Model):
	name = CharField()
	price = IntegerField()
	farmer = ForeignKeyField(Farmer, backref='foods')
  # need to make foreinKeyField() -- farmer
	created_at: DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Farmer, Food], safe=True)
	print("Connected to DB. Created TABLES (if not already there)")
	DATABASE.close()

