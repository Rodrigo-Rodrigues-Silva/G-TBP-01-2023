from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client.datebase

client_collection = db["clients"]

room_collection = db["rooms"]

booking_collection = db["bookings"]
