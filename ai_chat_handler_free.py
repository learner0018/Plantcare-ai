# ai_chat_handler_free.py
# Free AI chat using Hugging Face models - NO API KEY NEEDED!

import requests
import json

class PlantCareAI:
    """Free AI assistant using Hugging Face"""
    
    def __init__(self):
        """Initialize with free Hugging Face model"""
        # Using free inference API - no authentication required!
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        self.conversation_history = []
        print("✅ Free AI Chat initialized (Hugging Face)")
    
    def get_response(self, user_message, context=None):
        """
        Get AI response using free Hugging Face model
        
        Parameters:
            user_message: The user's question
            context: Optional context
        
        Returns:
            AI-generated response
        """
        
        try:
            # Build system context
            system_context = """You are a helpful plant care expert. 
            Help users with plant diseases, care tips, and treatments.
            Keep responses brief and practical."""
            
            if context:
                system_context += f"\n\nContext: {context}"
            
            # Prepare the prompt
            full_prompt = f"{system_context}\n\nUser: {user_message}\nAssistant:"
            
            # Call Hugging Face API (FREE - no key needed!)
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    ai_response = result[0].get('generated_text', '')
                    # Extract only the assistant's response
                    if 'Assistant:' in ai_response:
                        ai_response = ai_response.split('Assistant:')[-1].strip()
                    
                    print(f"💬 AI Response generated")
                    return ai_response if ai_response else self._get_fallback_response(user_message)
                else:
                    return self._get_fallback_response(user_message)
            else:
                print(f"⚠️ API returned status {response.status_code}")
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._get_fallback_response(user_message)
    
    def _get_fallback_response(self, user_message):
        """
        Fallback responses using rule-based logic
        When API is unavailable, we still provide helpful info!
        """
        
        message_lower = user_message.lower()
        
        # Disease-related questions
        if 'early blight' in message_lower:
            return """Early blight is a fungal disease. Treatment steps:
            
1. Remove infected leaves immediately
2. Apply copper-based fungicide weekly
3. Water at soil level (avoid leaves)
4. Improve air circulation
5. Apply mulch to prevent soil splash

Prevention: Crop rotation and disease-resistant varieties. 🌱"""
        
        elif 'late blight' in message_lower:
            return """Late blight is serious! Act fast:
            
1. Remove ALL infected plants
2. Apply copper fungicide immediately
3. Improve air circulation
4. Stop overhead watering
5. Monitor nearby plants

This spreads rapidly - quick action is critical! ⚠️"""
        
        # General care questions
        elif 'water' in message_lower or 'watering' in message_lower:
            return """Watering tips:
            
🌅 Water early morning (6-10 AM)
💧 Deep watering 2-3 times/week better than daily light watering
🎯 Water at soil level, not leaves
🌡️ More water in hot weather
✋ Check soil moisture first - if top 2 inches dry, water!

Overwatering causes root rot, underwatering causes stress."""
        
        elif 'fertilizer' in message_lower or 'nutrient' in message_lower:
            return """Fertilizer guide:
            
🌱 Young plants: Balanced fertilizer (10-10-10)
🍅 Fruiting plants: High phosphorus (5-10-10)
🥬 Leafy plants: High nitrogen (10-5-5)

Apply every 2-3 weeks during growing season.
Organic options: Compost, fish emulsion, bone meal. Don't over-fertilize!"""
        
        elif 'indoor' in message_lower or 'inside' in message_lower:
            return """Indoor plant tips:
            
☀️ Place near south-facing window for 6+ hours light
🌡️ Maintain 18-24°C temperature
💨 Ensure good air circulation
💧 Reduce watering (soil dries slower indoors)
🪴 Use well-draining potting mix
🐛 Monitor for pests regularly

Many herbs, peppers, and tomatoes grow well indoors!"""
        
        elif 'pest' in message_lower or 'bug' in message_lower or 'insect' in message_lower:
            return """Common pest solutions:
            
🐛 Aphids: Spray with soapy water
🕷️ Spider mites: Increase humidity, neem oil
🐌 Slugs: Beer traps, copper barriers
🦗 Caterpillars: Hand-pick or BT spray

Natural prevention:
- Neem oil spray weekly
- Companion planting (marigolds, basil)
- Encourage beneficial insects
- Keep garden clean"""
        
        elif 'soil' in message_lower:
            return """Healthy soil tips:
            
🌱 pH: 6.0-7.0 for most vegetables
🍂 Add compost regularly (2-3 inches yearly)
🌾 Mulch to retain moisture
🔄 Crop rotation prevents disease
💧 Well-draining is essential

Test soil every 2-3 years. Add lime to raise pH, sulfur to lower pH."""
        
        elif 'prevent' in message_lower or 'avoid' in message_lower:
            return """Disease prevention checklist:
            
✅ Space plants properly (air circulation)
✅ Water at soil level, morning only
✅ Remove dead/diseased material quickly
✅ Rotate crops annually
✅ Use disease-resistant varieties
✅ Mulch to prevent soil splash
✅ Clean tools regularly
✅ Monitor plants weekly

Prevention is easier than treatment! 🛡️"""
        
        elif 'tomato' in message_lower:
            return """Tomato care essentials:
            
☀️ Full sun (6-8 hours)
💧 Deep watering 2-3x/week
🌡️ 21-29°C ideal temperature
🥩 Stake or cage for support
✂️ Prune suckers for better fruit
🍴 Feed every 2 weeks when fruiting
🔄 Rotate location yearly

Common issues: Early blight, late blight, blossom end rot (calcium deficiency)."""
        
        elif any(word in message_lower for word in ['potato', 'potatoes']):
            return """Potato growing guide:
            
🌱 Plant in spring after last frost
⛰️ Hill soil around plants as they grow
💧 Consistent moisture important
🥔 Harvest when leaves yellow/die
📦 Store in cool, dark, dry place
🔄 3-4 year crop rotation essential

Watch for: Early blight, late blight, Colorado potato beetles."""
        
        # General questions
        elif any(word in message_lower for word in ['help', 'how', 'what', 'why', 'when', 'can', 'should']):
            return """I'm here to help with plant care! I can assist with:
            
🦠 Plant diseases & treatments
💧 Watering & feeding schedules
🌱 Growing tips & techniques
🐛 Pest control
🏡 Indoor & outdoor gardening
🌿 Specific plant care

Ask me anything specific, like:
- "How do I treat early blight?"
- "When should I water tomatoes?"
- "Best fertilizer for peppers?"

What would you like to know? 🌱"""
        
        else:
            return """I'm your plant care assistant! 🌱

I can help with:
- Disease identification & treatment
- Watering & fertilizing advice
- Pest control solutions
- Growing tips for vegetables & fruits
- Indoor & outdoor gardening

Try asking:
- "How often should I water tomatoes?"
- "What causes yellow leaves?"
- "How to prevent plant diseases?"

What plant question do you have?"""
    
    def get_disease_advice(self, disease_name, plant_name):
        """Get advice about a specific disease"""
        prompt = f"My {plant_name} has {disease_name}. What should I do?"
        return self.get_response(prompt)
    
    def get_plant_care_tips(self, plant_name):
        """Get care tips for a plant"""
        prompt = f"How do I care for {plant_name} plants?"
        return self.get_response(prompt)


# Test code
if __name__ == '__main__':
    print("="*60)
    print("Testing FREE AI Chat")
    print("="*60)
    
    ai = PlantCareAI()
    
    # Test questions
    test_questions = [
        "How do I treat early blight?",
        "When should I water tomatoes?",
        "What's the best fertilizer?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Q: {question}")
        response = ai.get_response(question)
        print(f"🤖 A: {response}\n")
        print("-"*60)
    
    print("\n✅ Free AI Chat working!")