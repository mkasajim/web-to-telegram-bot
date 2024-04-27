from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the URI, username, and password from the environment
uri = os.getenv('DB_URI')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Create a new client and connect to the server with authentication
client = MongoClient(uri, username=username, password=password)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client['url_changes']  # Database name
    collection = db['url_data']  # Collection name
    print(list(collection.find({})))
except Exception as e:
    print(e)