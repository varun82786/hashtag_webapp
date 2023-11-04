from pymongo import MongoClient
import hashlib
import base64
import bcrypt
import certifi

# Replace <username> and <password> with your actual MongoDB Atlas credentials
username = "edith"
password = "varun82786"
database_name = "eager"  # Replace with the name of your desired database

# Construct the MongoDB connection URI
uri = f"mongodb+srv://{username}:{password}@{database_name}.1dozl2p.mongodb.net/?retryWrites=true&w=majority"

# MongoDB connection
client = MongoClient(uri,tlsCAFile=certifi.where())
db = client[database_name]
users_collection = db['auth']

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_password_valid(entered_password, stored_hashed_password):
    # Check if the entered password matches the stored hashed password
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)

def signup_user(user_data):
    # Check if username already exists
    existing_user = users_collection.find_one({"username": user_data["username"]})
    if existing_user:
        return "Username already exists"
    
    # Hash the password before storing it
    hashed_password = hash_password(user_data["password"])
    user_data["password"] = hashed_password
    
    # Insert the new user data
    result = users_collection.insert_one(user_data)
    return "User signed up successfully"

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if not user:
        return "User not found"
    
    if is_password_valid(password, user["password"]):
        return "Login successful"
    else:
        return "Incorrect password"

# Example user data
new_user_data = {
    "unique_id": "SomeUniqueID",
    "username": "new_user",
    "user_no": 3,
    "emailid": "new_user@gmail.com",
    "name": "New User",
    "password": "sdfnkjs",
    "privilege": "normal"
}

# Sign up new user
signup_result = signup_user(new_user_data)
print(signup_result)

# Login user
login_result = login_user("new_user", "sdfnkjs")
print(login_result)



import pymongo

# Set up MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["your_database_name"]  # Replace with your database name
collection = db["your_collection_name"]  # Replace with your collection name

# Retrieve all documents and extract hashtags
hashtags_list = []
documents = collection.find({}, {"hashtag": 1})

for document in documents:
    hashtags_list.append(document["hashtag"])

# Close the MongoDB connection
client.close()

# Print the list of hashtags
print(hashtags_list)


