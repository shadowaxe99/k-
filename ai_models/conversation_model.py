```python
import openai
from config.config import OPENAI_API_KEY
from database.models import Conversation

class ConversationModel:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def create_conversation(self, user_id, influencer_id):
        # Initialize a new conversation in the database
        conversation = Conversation(user_id=user_id, influencer_id=influencer_id, messages=[])
        conversation.save()
        return conversation

    def add_message_to_conversation(self, conversation_id, sender, message):
        # Retrieve the conversation from the database
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            # Append the new message to the conversation
            conversation.messages.append({'sender': sender, 'message': message})
            conversation.save()
            return True
        return False

    def generate_ai_response(self, conversation_id):
        # Retrieve the conversation from the database
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            # Extract the conversation history
            conversation_history = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in conversation.messages])
            # Generate the AI response using OpenAI's GPT-3
            response = openai.Completion.create(
                engine="davinci",
                prompt=conversation_history,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.9
            )
            # Add the AI response to the conversation
            self.add_message_to_conversation(conversation_id, 'ai_influencer', response.choices[0].text.strip())
            return response.choices[0].text.strip()
        return "Could not generate a response."

    def get_conversation_history(self, conversation_id):
        # Retrieve the conversation from the database
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            return conversation.messages
        return []

# Example usage:
# conversation_model = ConversationModel()
# conversation = conversation_model.create_conversation(user_id=1, influencer_id=1)
# conversation_model.add_message_to_conversation(conversation.id, 'fan', 'OMG Kylie! I am such a huge fan!')
# ai_response = conversation_model.generate_ai_response(conversation.id)
# print(ai_response)
```