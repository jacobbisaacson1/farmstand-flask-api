from peewee import *
import datetime

DATABASE = SqliteDatabase('foods.sqlite')

class Food(Model):
	name = CharField()
	price = IntegerField()
	farmer = CharField() 
  # need to make foreinKeyField() -- farmer
	created_at: DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Food], safe=True)
	print("Connected to DB. Created TABLES (if not already there)")
	DATABASE.close()