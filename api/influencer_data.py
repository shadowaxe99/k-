from flask import Blueprint, jsonify
from database.models import Influencer
from database.database_connection import executeQuery

influencer_data_blueprint = Blueprint('influencer_data_blueprint', __name__)

@influencer_data_blueprint.route('/api/influencer/data/<influencer_name>', methods=['GET'])
def get_influencer_data(influencer_name):
    try:
        influencer = executeQuery(f"SELECT * FROM Influencer WHERE name = '{influencer_name}'")
        if influencer:
            return jsonify({
                'status': 'success',
                'data': {
                    'name': influencer.name,
                    'description': influencer.description,
                    'content': influencer.content
                }
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Influencer not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Pre-populate the database with Kylie Jenner's data
def initialize_influencer_data():
    influencer_name = "Kylie Jenner"
    influencer_description = ("Kylie Jenner is a glamorous and trendsetting personality with an edgy, "
                              "confident demeanor. She engages her audience in an aspirational, "
                              "lifestyle-focused way by showcasing her latest fashion, beauty products, "
                              "and luxurious surroundings. Kylie comes across as ambitious and "
                              "entrepreneurial, frequently promoting her highly successful businesses.")
    influencer_content = ("Kylie's Instagram (@kyliejenner) showcases her life as an influencer, model, "
                          "and businesswoman. Her content includes glamorous selfies, product promotion "
                          "for her makeup and skincare lines, and glimpses into her lavish lifestyle of "
                          "luxury travel, high fashion, and exclusive events.")
    
    # Check if the influencer already exists in the database
    existing_influencer = executeQuery(f"SELECT * FROM Influencer WHERE name = '{influencer_name}'")
    if not existing_influencer:
        # Insert Kylie Jenner's data into the Influencer table
        executeQuery(f"INSERT INTO Influencer (name, description, content) VALUES "
                     f"('{influencer_name}', '{influencer_description}', '{influencer_content}')")