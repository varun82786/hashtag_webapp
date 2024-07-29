from flask import Flask, render_template, request, redirect, url_for, session

#user defined libs
from scripts.operationsAPIs import operationsAPI 
from scripts.mongoAPI import mongoAPI

app = Flask(__name__)

app.config['TIMEOUT'] = 240  # Set the timeout to 120 seconds

app.secret_key = operationsAPI.generate_secret_key()  # Set a secret key for session management
"""
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
    global authenticated  # Use the global variable

    if request.method == 'POST':
        # Process login form data and authenticate user
        #credentials_data = operationsAPI.load_credentials_data()
        username = request.form['username']
        password = request.form['password']
        
        user = mongoAPI.auth_collection.find_one({"username": username})
        # Check if username and password match
        if user and operationsAPI.is_password_valid(password,user['password']):
            session['username'] = username  # Store the username in the session
            # Redirect to generator page
            return redirect(url_for('generator', username=username))

        # Authentication failed, show error message 
        return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')
"""

# Generator page
@app.route('/', methods=['GET', 'POST'])
def generator():
    """
    if 'username' not in session:
        return redirect(url_for('landing'))  # Redirect to login if user is not authenticated
    """
    if request.method == 'POST':
        # Process hashtag generation form data
        #hashtags_data = operationsAPI.load_hashtags_data()
        #hashtags_data=[document["hashtag"] for document in mongoAPI.hashtag_collection.find({}, {"hashtag": 1, "parameters": 1})]
        data_basedocument = mongoAPI.hashtag_collection.find({}, {"hashtag": 1, "parameters": 1, "gener": 1})

        hashtags_data = []
        parameter_data = []
        gener_data = []

        for document in data_basedocument:
            hashtags_data.append(document["hashtag"])
            parameter_data.append(document["parameters"])
            gener_data.append(document["gener"])
                    
        hashtags = request.form['hashtags']
        generated_hashtags = []

        # Split input into individual hashtags
        input_hashtags = operationsAPI.remove_empty_elements([tag.strip() for tag in hashtags.split(' ')])

        # Generate hashtags based on input
        generated_tags =  operationsAPI.generate_hashtags(input_hashtags,hashtags_data, parameter_data, gener_data)
        generated_hashtags = generated_tags[0]
        #gener_generated_hashtags = generated_tags[1]
        
        if generated_hashtags:
            return render_template('generator.html', input_hashtags = input_hashtags, generated_hashtags = generated_hashtags)#, gener_generated_hashtags = gener_generated_hashtags)
        else:
            return render_template('generator.html')

    return render_template('generator.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
