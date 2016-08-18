from flask import Flask, render_template, request
from flask_pymongo import PyMongo

## Setup
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test_db'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
mongo = PyMongo(app)

## Route
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		return get_result(request.form)
	else:
		return view()
		
## Operation
def view():
	return render_template('index.html', is_result=False)

def get_result(form):
	map = {
		'artist-name' : 'name',
		'artist-alias' : 'aliases.name',
		'tags' : 'tags.value'
	}
	
	condition = {}
	
	for key, value in map.items():
		if form[key] and form[key].strip() != '':
			condition[value] = form[key]
	
	artist_results = mongo.db.artists.aggregate([
		{ '$match' : condition },
		{ '$sort' : { 'rating.value' : -1 } },
		{ '$limit' : 10 }
	])
	
	artists = [artist for artist in artist_results]
	
	return render_template('index.html', is_result=True, artists=artists, form=form)
	

if __name__ == '__main__':
	app.run()