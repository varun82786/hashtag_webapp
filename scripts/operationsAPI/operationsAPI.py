import json
import random
import string
import bcrypt
import secrets
import time
import sys
sys.path.append(r'scripts')
from mongoAPI import mongoAPI

# Define JSON file paths as global variables
CREDENTIALS_JSON_PATH= r'database/authorization/auth/auth.json'
HASHTAG_JSON_PATH  = r'database/source_data/street_photography/hashtagDB.json'

def generate_random_string(length):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

# Load hashtags data from JSON file
def load_hashtags_data():
    with open(HASHTAG_JSON_PATH) as file:
        hashtags_data = [hashtag for hashtag in json.load(file)]
    return hashtags_data

# Load credentials data from JSON file
def load_credentials_data():
    with open(CREDENTIALS_JSON_PATH) as file:
        credentials_data = json.load(file)
    return credentials_data

# Update credentials data in JSON file
def update_credentials_data(credentials_data):
    existing_credentials_data = load_credentials_data()

    # Append new data to existing credentials object
    existing_credentials_data.update(credentials_data)

    # Update credentials JSON file
    with open(CREDENTIALS_JSON_PATH, 'w') as file:
        json.dump(existing_credentials_data, file, indent=4)

## Remove empty elements in the list 
def remove_empty_elements(input_list):
    return [item for item in input_list if item]

## Generate hashtags based on input and return the random of the hashtag list    
def generate_hashtags(input_hashtags, hashtags_data):
    # Convert input hashtags to a set for faster membership checking
    input_hashtags_set = {input_tag.lower() for input_tag in input_hashtags}
    
    # Create a generator function to yield hashtags one at a time in both directions
    def generate_bidirectional_hashtags():
        for data_tag in hashtags_data:
            if data_tag.lower() in input_hashtags_set:
                print(f"Fetching details for {data_tag}")
                hashtag_details = mongoAPI.doc_details(mongoAPI.hashtag_collection, data_tag)
                occurrence = hashtag_details.get("parameters")[0]
                yield f'#{data_tag} {occurrence}'
        for input_tag in input_hashtags:
            for data_tag in hashtags_data:
                if input_tag.lower() in data_tag.lower():
                    print(f"Fetching details for {data_tag}")
                    hashtag_details = mongoAPI.doc_details(mongoAPI.hashtag_collection, data_tag)
                    occurrence = hashtag_details.get("parameters")[0]
                    yield f'#{data_tag} {occurrence}'

    # Shuffle and yield generated hashtags one at a time
    generated_hashtags = list(generate_bidirectional_hashtags())
    random.shuffle(generated_hashtags)

    return set(generated_hashtags)

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_password_valid(entered_password, stored_hashed_password):
    # Check if the entered password matches the stored hashed password
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)

#print(load_hashtags_data())

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


# lis = ["skyphotography", "worldphotographyday" ,"ballaratphoto" ,"officialphotographyhub" ,"traveldiary" ,"thephotographyblogger"  ]

# for hash in lis:
#     generate_hashtags()