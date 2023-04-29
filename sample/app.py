from flask import Flask, render_template 

app = Flask(__name__)

# @app.route('/')
# def welcome():
#     return render_template('index.html')

@app.route('/')
def index():
	hashtags = ['travel', 'nature', 'food']
	return render_template('index.html', hashtags=hashtags)

if __name__ == '__main__':
    app.run(debug=True)