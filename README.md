# ⭐ This script is utilizing discord.py-self and OpenAI's API to make AI respond to your private messages! ⭐
#### The !toggle_ai command isn't working until i fix it, so the script is going to respond to your dms until you stop the script
## Features: 
    Responds to direct messages with AI-generated text based on user input.
    Caches user messages and periodically sends responses based on collected input.

## Setup Instructions
### Prerequisites
 #### Python 3.8 or higher

 #### Discord API token

#### OpenAI API key

### Installation
 #### Clone the repository:
    
    1. git clone https://github.com/netnsher/selfai.git
    
    2. cd selfai

### Install dependencies:

    pip install discord.py-self openai asyncio

### Configuration

    Obtain your Discord API token and OpenAI API key.
    Replace placeholders in the script (DISCORD_TOKEN and OPENAI_API_KEY) with your actual tokens:

    DISCORD_TOKEN = "your_discord_token_here"
    OPENAI_API_KEY = "your_openai_api_key_here"

### Running the Bot
``` python selfai.py ```
### Bot Usage

  
  If someone dms you while  the script is running it will respond based on the conversation history and base prompts.

### Customizing Base Prompts

    Locate the base_prompt variable in the handle_ai_response method of MyClient class.
    Customize the base prompt to tailor the bot's responses based on your requirements:


    base_prompt = (
        "Your custom base prompt here..."
    )

        Include specific details and instructions on how you want the bot to respond.
        Ensure the prompt reflects the tone and style you want the AI to use.

### Troubleshooting

    If the bot encounters issues, check the console output for error messages.
    Or open an issue 

