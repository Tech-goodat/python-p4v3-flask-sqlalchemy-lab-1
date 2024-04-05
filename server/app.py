# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakeByID(id):
    earthquake=Earthquake.query.filter(Earthquake.id==id).first()
    if earthquake:
        body={
            "id":earthquake.id,
            "location":earthquake.location,
            "magnitude":earthquake.magnitude,
            "year":earthquake.year
            }
        status=200

    else:
        body={'message': f'earthquake {id} not found.'}
        status=404

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:min_magnitude>')
def min_magnitude(min_magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= min_magnitude).limit(3).all()
    if earthquakes:
        quake_list = [{
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        } for earthquake in earthquakes]
        body = {
            "count": len(earthquakes),
            "quakes": quake_list
        }
        status = 200
    else:
        body = {
            'message': f'No earthquakes found with magnitude greater than or equal to {min_magnitude}'
        }
        status = 404

    return make_response(body, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
