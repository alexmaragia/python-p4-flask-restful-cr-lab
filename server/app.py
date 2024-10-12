#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = db.session.get(Plant, id)
    if plant:
        return jsonify(plant.to_dict())
    return jsonify({"error": "Plant not found"}), 404

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    
    if not all(key in data for key in ('name', 'image', 'price')):
        return jsonify({"error": "Missing required fields"}), 400
    
    if not data['image'].startswith(('http://', 'https://')):
        return jsonify({"error": "Image URL must be an absolute URL"}), 400
    
    try:
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=float(data['price'])
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201
    except ValueError:
        return jsonify({"error": "Invalid price format"}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)