from pymongo import MongoClient
import certifi

connection = MongoClient('mongodb+srv://luisramosmatas:lrmtfg2122@cluster0.vu97h.mongodb.net/PCM?retryWrites=true&w=majority', tlsCAFile=certifi.where())