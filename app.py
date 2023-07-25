from flask import Flask, render_template, request, redirect, url_for
import json
import random
import string

app = Flask(__name__)

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

# Landing page - Signup or Login
@app.route('/')
def landing():
    return render_template('landing.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process signup form data and update credentials
        credentials_data = load_credentials_data()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        #print(username)
        # Check if username or email already exists
        if username in credentials_data or any(data.get('emailid') == email for data in credentials_data.values()):
            return render_template('signup.html', error='Username or email already exists.')

        # Add new user credentials
        user_id = generate_random_string(10) 
        user_no=str(len(credentials_data) + 1)
        credentials_data[username] = {
            'unique_id': user_id,
            'user_no'  : user_no,
            'emailid'  : email,
            'password' : password,
            'privilege': 'normal'
            
        }
        print(credentials_data)
        # Update credentials JSON file
        update_credentials_data(credentials_data)

        # Redirect to login page
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data and authenticate user
        credentials_data = load_credentials_data()
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match
        if username in credentials_data and credentials_data[username]['password'] == password:
            # Redirect to generator page
            return redirect(url_for('generator'))

        # Authentication failed, show error message
        return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

# Generator page
@app.route('/generator', methods=['GET', 'POST'])
def generator():
    if request.method == 'POST':
        # Process hashtag generation form data
        hashtags_data = load_hashtags_data()
        hashtags = request.form['hashtags']
        generated_hashtags = []

        # Split input into individual hashtags
        input_hashtags = [tag.strip() for tag in hashtags.split(',')]

        # Generate hashtags based on input
        for input_tag in input_hashtags:
            for data_tag in hashtags_data:
                if input_tag.lower() in data_tag.lower() or data_tag.lower() in input_tag.lower():
                    generated_hashtags.append(data_tag)
                    #break  # Break out of inner loop if a match is found
        #print(generated_hashtags)
        if generated_hashtags:
            return render_template('generator.html', input_hashtags=input_hashtags, generated_hashtags=generated_hashtags)
        else:
            return render_template('generator.html')

    return render_template('generator.html')

#if __name__ == '__main__':
#     app.run(host="0.0.0.0",port=80,debug=True)
