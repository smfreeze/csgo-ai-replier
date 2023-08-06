import json
import requests
import sys


HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'
character = 'Gamer'

def getResponse(user_input):
    history = {'internal': [], 'visible': []} # Change if you want to use history
    
    request = {
        'user_input': user_input,
        'max_new_tokens': 750,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'chat',
        'character': character, # Change/add this in the oogabooga api (chat settings -> character)
        'instruction_template': 'Vicuna-v1.1', 
        'your_name': 'You',
        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|Character|>".\n\n<|Prompt|>',
    }

    try:
        response = requests.post(URI, json=request)
        if response.status_code == 200:
            try:
                result = response.json()['results'][0]['history']['visible'][-1][1]
                return result
            except (KeyError, json.JSONDecodeError):
                print("Invalid response data format.\nMake sure your character is saved as .yaml (use web ui to make a character if you have not already!)")
    except Exception as e:
        print("No connection to oogabooga server on URI " + URI)
        sys.exit(1)
