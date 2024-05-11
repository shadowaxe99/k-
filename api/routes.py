from flask import Blueprint, request, jsonify
from ai_models.conversation_model import generateConversation
from ai_models.persona_model import generatePersona
from ai_models.features_model import generateFeatures
from api.auth import authenticateRequest
from api.exceptions import ValidationError
from utils.validators import validate_conversation_input, validate_feature_input
from database.models import User, Influencer, Conversation, Feature

routes = Blueprint('routes', __name__)

@routes.route('/api/conversation', methods=['POST'])
@authenticateRequest
def api_conversation():
    try:
        data = request.json
        validate_conversation_input(data)
        user_id = data['user_id']
        influencer_id = data['influencer_id']
        message = data['message']
        
        # Fetch influencer data from the database
        influencer = Influencer.query.get(influencer_id)
        if not influencer:
            raise ValidationError("Influencer not found.")
        
        # Generate a response using the AI model
        response = generateConversation(influencer.name, message)
        
        # Save the conversation to the database
        conversation = Conversation(user_id=user_id, influencer_id=influencer_id, messages=[message, response])
        conversation.save()
        
        return jsonify({'status': 'success', 'message': response}), 200
    except ValidationError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@routes.route('/api/persona', methods=['GET'])
def api_persona():
    influencer_name = request.args.get('influencer_name')
    influencer = Influencer.query.filter_by(name=influencer_name).first()
    if influencer:
        persona = generatePersona(influencer.description)
        return jsonify({'status': 'success', 'persona': persona}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Influencer not found'}), 404

@routes.route('/api/features', methods=['POST'])
@authenticateRequest
def api_features():
    try:
        data = request.json
        validate_feature_input(data)
        feature_name = data['feature_name']
        user_id = data['user_id']
        
        # Generate feature content using the AI model
        feature_content = generateFeatures(feature_name)
        
        # Save the feature interaction to the database
        feature = Feature(name=feature_name, description=feature_content, user_id=user_id)
        feature.save()
        
        return jsonify({'status': 'success', 'feature_content': feature_content}), 200
    except ValidationError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@routes.route('/api/influencer/data', methods=['GET'])
def api_influencer_data():
    influencer_name = request.args.get('influencer_name')
    influencer = Influencer.query.filter_by(name=influencer_name).first()
    if influencer:
        return jsonify({
            'status': 'success',
            'influencer_data': {
                'name': influencer.name,
                'description': influencer.description,
                'content': influencer.content
            }
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Influencer not found'}), 404

# Additional routes for user login, registration, subscription, and payment processing can be added here
# ...

# Register the blueprint in the main application
# app.register_blueprint(routes) (This line would be in main.py)