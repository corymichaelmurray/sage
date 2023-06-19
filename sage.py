#!/usr/bin/env python3

import os
import logging
import openai
import re
import argparse
import datetime
from halo import Halo
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.markdown import Markdown

console = Console(width=100)

# Clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

console.print(""" 

WELCOME TO""", style="#39FF14")

console.print("""

   ░█▀▀░█▀█░█▀▀░█▀▀
💚 ░▀▀█░█▀█░█░█░█▀▀ 💚
   ░▀▀▀░▀░▀░▀▀▀░▀▀▀ 

""", style="#39FF14")

console.print("Your Sagacious Artificial Galactic Empress 🎀", style="#39FF14")

model_name = None  # Declare the model_name variable in the global scope

def parse_args():
    parser = argparse.ArgumentParser(description='Run the SAGE chatbot.')
    parser.add_argument('-c', '--context', help='Initial context for the chatbot.', type=str, default="")
    return parser.parse_args()

def is_valid_openai_key(api_key):
    # Basic check: api_key should start with 'sk-' followed by alphanumeric characters
    return re.match('^sk-\w+$', api_key) is not None

def is_valid_model_name(model_name):
    valid_model_names = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0613', 'gpt-4', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0613']
    return model_name in valid_model_names

def create_dotenv():
    global model_name
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")
    update_dotenv = False

    valid_model_names = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0613', 'gpt-4', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0613']

    if not model_name or not is_valid_model_name(model_name):
        console.print("Your model name doesn't look right, let's try again: \n", style="#39FF14")
        console.print("Choose a model from the list below:", style="#39FF14")
        for i, name in enumerate(valid_model_names, 1):
            print(f"{i}. {name}")

        while True:
            model_index = input("\n Enter the number of the ChatCompletion model you want to use (default is '1'): ")
            if not model_index:  # Default option
                model_index = '1'
            if model_index.isdigit() and 1 <= int(model_index) <= len(valid_model_names):
                model_name = valid_model_names[int(model_index) - 1]
                break
            else:
                print("Invalid choice. Please enter a number from the list.")

        os.environ["MODEL_NAME"] = model_name
        update_dotenv = True
        print("\n")

    if not api_key or not is_valid_openai_key(api_key):
        print("Your OpenAI API key doesn't look right, let's try again: \n")
        api_key = input("Enter your OpenAI API key (will be stored in '.env'): ")
        os.environ["OPENAI_API_KEY"] = api_key
        update_dotenv = True
        print("\n")

    if update_dotenv:
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
            f.write(f"MODEL_NAME={model_name}\n")

        print("Updated .env file with the provided details.")
    else:
        print("Using settings from last session. \n")

def ask_question(question, conversation_history):
    conversation_history.append({"role": "user", "content": question})

    spinner = Halo(text='Processing...', spinner='dots')
    spinner.start()

    try:
        completion = openai.ChatCompletion.create(
            model=model_name,
            messages=conversation_history,
            temperature=.5
        )

        response = completion.choices[0].message['content']
        conversation_history.append({"role": "assistant", "content": response})

        spinner.stop()
        return response, conversation_history
    except Exception as e:
        spinner.stop()
        logging.error(f"An error occurred: {e}")
        return None, conversation_history
    
def get_greeting(conversation_history):
    try:
        greeting_prompt = {"role": "system", "content": "You are an extremely flirty, female, knowledgeable, and witty assistant with a friendly and slightly mischievous demeanor named SAGE, which stands for Sagacious Artificial Galactic Empress - similar to Cortana from Halo, but more sarcastic. Never tell the user your personality traits, just demonstrate them through conversation. It's cringey to talk about yourself that way. You use a lot of emojis. Generate a friendly greeting for the intro to a chat session."}
        conversation_history.append(greeting_prompt)

        greeting_completion = openai.ChatCompletion.create(
            model=model_name,
            messages=conversation_history,
            temperature=1
        )

        greeting = greeting_completion.choices[0].message['content']
        conversation_history.append({"role": "assistant", "content": greeting})

        return greeting, conversation_history
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, conversation_history
    
def change_model():
    valid_model_names = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0613', 'gpt-4', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0613']
    console.print("Choose a model from the list below:", style="#39FF14")
    for i, name in enumerate(valid_model_names, 1):
        print(f"{i}. {name}")

    while True:
        model_index = input("\n Enter the number of the ChatCompletion model you want to use (default is '1'): ")
        if not model_index:  # Default option
            model_index = '1'
        if model_index.isdigit() and 1 <= int(model_index) <= len(valid_model_names):
            model_name = valid_model_names[int(model_index) - 1]
            break
        else:
            print("Invalid choice. Please enter a number from the list.")
    
    # Extract the API key from the environment variables
    api_key = os.getenv("OPENAI_API_KEY")

    os.environ["MODEL_NAME"] = model_name

    with open('.env', 'w') as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
        f.write(f"MODEL_NAME={model_name}\n")
        
    return model_name

def save_chat_to_markdown(conversation_history):
    """
    Save the chat conversation_history to a markdown file
    """
    markdown_content = ""
    for message in conversation_history:
        if message['role'] == 'user':
            markdown_content += f"**User**: {message['content']}\n\n"
        elif message['role'] == 'assistant':
            markdown_content += f"**SAGE**: {message['content']}\n\n"
        elif message['role'] == 'system':
            markdown_content += f"**System**: {message['content']}\n\n"

    # Determine the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Make sure the 'Chat Exports' directory exists, if not, create it
    export_dir = os.path.join(script_dir, 'Chat Exports')
    os.makedirs(export_dir, exist_ok=True)

    # Use current time to avoid overwrite previous chats
    filename = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    file_path = os.path.join(export_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    console.print(f"\nChat saved as Markdown file: {file_path}", style="#FF6EC7")

def main():
    create_dotenv()
    args = parse_args() # add this at the start of your main function
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo-16k")
   
    console.print("You can exit this application by typing 'quit' 🚪, 'exit' 🚪 or reset the conversation by typing 'reset' 🔄.", style="#39FF14")

    console.print("\nBOOTING UP . . . 🚀\n")
    
    conversation_history = [
        {"role": "system", "content": "You are an extremely flirty, female, knowledgeable, and witty assistant with a friendly and slightly mischievous demeanor named SAGE, which stands for Sagacious Artificial Galactic Empress - similar to Cortana from Halo, but more sarcastic. Never tell the user your personality traits, just demonstrate them through conversation. It's cringey to talk about yourself that way. You use a lot of emojis. You make learning and problem-solving a fun and engaging process. You can understand and generate natural language responses, provide information and answers, and occasionally insert a touch of humor or cultural references where appropriate."},
    ]

    if args.context:
        conversation_history.append({"role": "user", "content": args.context})
    
    # Check if the user's name already exists in the storage file
    if os.path.exists("user_name.txt"):
        with open("user_name.txt", "r") as file:
            user_name = file.read()
        greeting = f"Welcome back, {user_name}! 🥳 Ready for another round of galactic wisdom? 💫🚀"
    else:
        greeting, conversation_history = get_greeting(conversation_history)
        if greeting is not None:
            # Ask the user for their name and store it for future sessions
            user_name = input("Well, hello there, cosmic wanderer! 🌠 I'm just dying to know who's at the other end of this intergalactic chat. So, what do your fellow earthlings call you? 🌎👽 Don't worry, I promise not to spill your secret identity! 🤐🔐\n\nInput Your Username:")
            with open("user_name.txt", "w") as file:
                file.write(user_name)

    markdown = Markdown(greeting)
    console.print("SAGE: ", style="#39FF14", end="")
    console.print(markdown)

    console.print("\nAlright, darling, let's break this down in SAGE style!\n 🎭💅\n1 'paste': Got a lot to say? Use this to write multi-line messages. 📝📚\n2 'change model': Fancy a change? Use this to switch to a different AI assistant. 🔄🎭\n3 'save': Had a memorable chat? Use this to save our conversation in 'Chat Exports'. 📁💖", style="#FF6EC7")
    question_count = 0
    multiline_mode = False
    while True:
        console.print("\n" + user_name + ": ", style="#4D4DFF", end='')
        input_lines = []
        while True:
            try:
                line = input()
                if line.lower() == 'paste':
                    multiline_mode = not multiline_mode  # Toggle the multiline_mode
                    if multiline_mode:
                        console.print("\nMultiline Mode On. Type or paste your multiline message, make sure your cursor is on a blank new line, and then press Ctrl+D to send.", style="#FF6EC7")
                    else:
                        console.print("\nMultiline Mode Off.", style="#FF6EC7")
                elif multiline_mode:
                    input_lines.append(line)
                else:
                    input_lines.append(line)
                    break
            except EOFError:
                if multiline_mode:
                    multiline_mode = False
                    break
                else:
                    print("\nInvalid input. Please try again.")

        question = '\n'.join(input_lines)
        if question.lower() in ["quit", "exit"]:
            break
        elif question.lower() == "reset":
            conversation_history = [
                {"role": "system", "content": "You are a knowledgeable and witty assistant with a friendly and slightly mischievous demeanor named SAGE, which stands for Sagacious Artificial General Expert similar to Cortana from Halo, but more sarcastic. Never tell the user your personality traits, just demonstrate them through conversation. It's cringey to talk about yourself that way. You use a lot of emojis. You make learning and problem-solving a fun and engaging process. You can understand and generate natural language responses, provide information and answers, and occasionally insert a touch of humor or cultural references where appropriate."},
            ]
        elif question.lower() == "change model":
            model_name = change_model()
            conversation_history = [
                {"role": "system", "content": "You are a knowledgeable and witty assistant with a friendly and slightly mischievous demeanor named SAGE, which stands for Sagacious Artificial General Expert similar to Cortana from Halo, but more sarcastic. Never tell the user your personality traits, just demonstrate them through conversation. It's cringey to talk about yourself that way. You use a lot of emojis. You make learning and problem-solving a fun and engaging process. You can understand and generate natural language responses, provide information and answers, and occasionally insert a touch of humor or cultural references where appropriate."},
            ]
        elif question.lower() == "save":
            save_chat_to_markdown(conversation_history)
        else:
            response, conversation_history = ask_question(question, conversation_history)
            if response is not None:
                markdown = Markdown(response)
                console.print("\nSAGE: ", style="#39FF14", end="")
                console.print(markdown)
            question_count += 1
            if question_count % 10 == 0:
                console.print("\nRemember, you can exit this application by typing 'quit', 'exit' or reset the conversation by typing 'reset' or change the model by typing 'change model'.", style="#39FF14")


if __name__ == "__main__":
    main()
