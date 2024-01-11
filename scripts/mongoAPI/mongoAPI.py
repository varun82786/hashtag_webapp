import sys
sys.path.append(r'scripts')

from mongoAPI import mongodb_init 
import bcrypt

Client = mongodb_init.server_check()

# Replace "your_collection_name" with the name of your desired collection
auth_collection = Client["eager"]["auth"]
hashtag_collection = Client["eager"]["hashtag_dev2"]



# sign up and login operations

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
    existing_user = auth_collection.find_one({"username": user_data["username"]})
    if existing_user:
        return "Username already exists"
    
    # Hash the password before storing it
    hashed_password = hash_password(user_data["password"])
    user_data["password"] = hashed_password
    
    # Insert the new user data
    result = auth_collection.insert_one(user_data)
    return "User signed up successfully"

def login_user(username, password):
    user = auth_collection.find_one({"username": username})
    if not user:
        return "User not found"
    
    if is_password_valid(password, user["password"]):
        return "Login successful"
    else:
        return "Incorrect password"


# CRUD Operations

def create_document(collection, data):
    try:
        result = collection.insert_one(data)
        print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print("Error creating document:", e)

def read_documents(collection, filter_query=None):
    try:
        documents = collection.find(filter_query) if filter_query else collection.find()
        for doc in documents:
            print(doc)
        return documents
    except Exception as e:
        print("Error reading documents:", e)

def update_document(collection, filter_query, update_data):
    try:
        result = collection.update_one(filter_query, {"$set": update_data})
        print(f"Modified {result.modified_count} document(s).")
    except Exception as e:
        print("Error updating document:", e)

def delete_document(collection, filter_query):
    try:
        result = collection.delete_one(filter_query)
        print(f"Deleted {result.deleted_count} document.")
    except Exception as e:
        print("Error deleting document:", e)

def doc_details(collection= hashtag_collection,hashtag="None"):
    result = collection.find_one({"hashtag": hashtag}, {"category": 1, "gener": 1, "location": 1, "parameters": 1})
    #print(result)
    return result

# lis = ["skyphotography", "worldphotographyday" ,"ballaratphoto" ,"officialphotographyhub" ,"traveldiary" ,"thephotographyblogger"  ]

# for hash in lis:
#     print(doc_details(hashtag_collection,hash))

#read_documents(auth_collection)