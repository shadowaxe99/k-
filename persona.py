```python
from ai_models.persona_model import generatePersona

class Persona:
    def __init__(self, influencer_name, influencer_description, influencer_content):
        self.influencer_name = influencer_name
        self.influencer_description = influencer_description
        self.influencer_content = influencer_content
        self.persona_data = None

    def create_persona(self):
        # Use the generatePersona function from the persona_model to create the AI persona
        self.persona_data = generatePersona(self.influencer_description, self.influencer_content)

    def get_persona_data(self):
        if not self.persona_data:
            self.create_persona()
        return self.persona_data

# Example usage:
# influencer_name = "Kylie Jenner"
# influencer_description = "Kylie Jenner is a glamorous and trendsetting personality with an edgy, confident demeanor. She engages her audience in an aspirational, lifestyle-focused way by showcasing her latest fashion, beauty products, and luxurious surroundings. Kylie comes across as ambitious and entrepreneurial, frequently promoting her highly successful businesses."
# influencer_content = "Kylie's Instagram (@kyliejenner) showcases her life as an influencer, model, and businesswoman. Her content includes glamorous selfies, product promotion for her makeup and skincare lines, and glimpses into her lavish lifestyle of luxury travel, high fashion, and exclusive events."
# kylie_persona = Persona(influencer_name, influencer_description, influencer_content)
# persona_data = kylie_persona.get_persona_data()
# print(persona_data)
```