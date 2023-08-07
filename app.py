from flask import Flask, render_template, request, redirect, url_for

#user defined libs
from scripts.operationsAPI import operationsAPI 
from scripts.mongoAPI import mongoAPI

app = Flask(__name__)

# Landing page - Signup or Login
@app.route('/')
def landing():
    return render_template('landing.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process signup form data and update credentials
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        if mongoAPI.auth_collection.count_documents({'$or': [{'username': username}, {'emailid': email}]}) > 0:
            return render_template('signup.html', error='Username or email already exists.')

        # Add new user credentials
        user_id = operationsAPI.generate_random_string(10)
        user_no = str(mongoAPI.auth_collection.count_documents({}) + 1)
        credentials_data = {
            'unique_id': user_id,
            'username': username,
            'user_no': int(user_no),
            'emailid': email,
            'password': operationsAPI.hash_password(password),
            'privilege': 'normal'
        }
        mongoAPI.auth_collection.insert_one(credentials_data)

        # Redirect to login page
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data and authenticate user
        credentials_data = operationsAPI.load_credentials_data()
        username = request.form['username']
        password = request.form['password']
        
        user = mongoAPI.auth_collection.find_one({"username": username})
        # Check if username and password match
        if user and operationsAPI.is_password_valid(password,user['password']):
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
        hashtags_data = operationsAPI.load_hashtags_data()
        hashtags = request.form['hashtags']
        generated_hashtags = []

        # Split input into individual hashtags
        input_hashtags = [tag.strip() for tag in hashtags.split(',')]

        # Generate hashtags based on input
        generated_hashtags = operationsAPI.generate_hashtags(input_hashtags,hashtags_data)
        
        if generated_hashtags:
            return render_template('generator.html', input_hashtags=input_hashtags, generated_hashtags=generated_hashtags)
        else:
            return render_template('generator.html')

    return render_template('generator.html')

if __name__ == '__main__':
     app.run(host="0.0.0.0",port=80,debug=True)
