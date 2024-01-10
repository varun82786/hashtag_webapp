from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

# Replace <username> and <password> with your actual MongoDB Atlas credentials
username = "edith"
password = "varun82786"
database_name = "eager"  # Replace with the name of your desired database

# Construct the MongoDB connection URI
uri = f"mongodb+srv://{username}:{password}@{database_name}.1dozl2p.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
def server_check():
    client = MongoClient(uri, tlsCAFile=certifi.where())
    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!\n")
        return client
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None

# Call the function to test the connection
#client = server_check()

#server_check()

# Now you can use the 'client' object to interact with your MongoDB deployment
# For example, you can access databases and collections as follows:
# db = client[database_name]
# collection = db["your_collection_name"]
# collection.insert_one({"key": "value"})

# Don't forget to close the connection when you're done
#if client:
#    client.close()
