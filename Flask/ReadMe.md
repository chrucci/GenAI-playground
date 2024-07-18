# LiteLLM Interface with Advanced Settings

This Flask application provides a web interface for interacting with various Language Models (LLMs) using LiteLLM. It includes advanced settings for model parameters and integrates with Langfuse for tracking and analysis.

## Features

- Support for multiple LLMs including GPT models, Claude models, and Ollama models
- Advanced parameter settings (temperature, top_p, max_tokens)
- Conversation history with session management
- Predefined prompts for quick start
- User rating system for conversations
- Integration with Langfuse for tracking and analysis

## Setup

1. Install the required packages:
   ```
   pip install flask litellm langfuse python-dotenv
   ```

2. Set up your environment variables in a `.env` file:
   ```
   LANGFUSE_PUBLIC_KEY=your_public_key
   LANGFUSE_SECRET_KEY=your_secret_key
   LANGFUSE_HOST=https://cloud.langfuse.com
   OLLAMA_BASE_URL=your_ollama_base_url (if using Ollama models)
   ```

3. Run the Flask application:
   ```
   python claude.py
   ```

## Usage

1. Open a web browser and navigate to `http://localhost:5000`
2. Select an LLM from the dropdown menu
3. Enter your prompt in the text area or choose a predefined prompt
4. Adjust the model parameters if desired
5. Click "Submit" to send your prompt to the LLM
6. View the conversation history in the conversation area
7. Rate the conversation using the rating buttons
8. Use the "Reset Conversation" button to start a new conversation

## Files

- `claude.py`: The main Flask application file
- `templates/index.html`: The HTML template for the web interface

## Customization

You can customize the list of available LLMs and predefined prompts by modifying the `LLMS` and `PROMPTS` lists in `claude.py`.

## Note

Make sure to handle API keys and sensitive information securely in a production environment.
