import pymongo
from pymongo import MongoClient

class MongoWrapper:

	ressource_static = None

	def __init__(self, db_name="test_db"):
		""" Init Connection to MongoDB """
		if not MongoWrapper.ressource_static:
			self.ressource = MongoClient()
			MongoWrapper.ressource_static = self.ressource
		else:
			self.ressource = MongoWrapper.ressource_static
		self.db_name = db_name

	def useDB(self, db_name):
		self.db_name = db_name

	def getCollectionNames(self):
		return self.ressource[self.db_name].collection_names()

	def getDbs(self):
		return self.ressource.database_names()

	def getCollection(self, col_name):
		return self.ressource[self.db_name][col_name]

