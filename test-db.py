from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

username = "sandipan"
password = "k_S6BCM7NK2VwYc"

# Get the URI from the environment
DB_URI = f"mongodb+srv://sandipan:{password}@web-to-tg.0ozaqoa.mongodb.net/?retryWrites=true&w=majority&appName=web-to-tg"
uri = os.getenv('DB_URI')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
