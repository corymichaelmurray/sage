import os
import datetime
from rich.console import Console

console = Console()  # Create an instance of Console

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
