import random

# Simple knowledge base
knowledge_base = {
    "greeting": ["Hello!", "Hi there!", "Greetings!"],
    "farewell": ["Goodbye!", "Farewell!", "See you!"],
    "about_me": ["I am a chatbot designed to assist you.", "I'm just a computer program here to help."],
    "favorites": ["I don't have preferences, but I can provide information on various topics."],
    "default": ["I'm sorry, I didn't understand that. Can you please provide more details?"]
}

def get_response(user_input):
    # Analyze user input and generate a response
    if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
        return random.choice(knowledge_base["greeting"])
    elif any(word in user_input.lower() for word in ["bye", "goodbye"]):
        return random.choice(knowledge_base["farewell"])
    elif "how are you" in user_input.lower():
        return "I'm just a program, but I'm doing well. Thanks for asking!"
    elif "tell me about yourself" in user_input.lower():
        return random.choice(knowledge_base["about_me"])
    elif "favorites" in user_input.lower():
        return random.choice(knowledge_base["favorites"])
    else:
        return random.choice(knowledge_base["default"])

# Simple console-based interaction
print("Chatbot: Hello! Type 'bye' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'bye':
        print("Chatbot:", random.choice(knowledge_base["farewell"]))
        break
    response = get_response(user_input)
    print("Chatbot:", response)
