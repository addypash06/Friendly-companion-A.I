# Friendly Companion

A friendly AI chat companion built with Streamlit and Google's Gemini API. It is designed to listen to users' emotions and provide supportive, empathetic, and encouraging responses for everyday conversations, stress, sadness, anxiety, or happy moments.

## Features

- A warm, supportive conversational interface
- Emotional awareness and empathetic responses
- Encouraging motivational closing messages
- Conversation history preserved in session memory
- Sidebar controls for starting a fresh chat
- Clean, centered UI with a soft custom theme

## Tech Stack

- Python
- Streamlit
- Google GenAI SDK
- python-dotenv

## Project Structure

- `code.py` — main Streamlit application
- `.env` — local environment variables (not committed)
- `requirements.txt` — Python dependencies

## Requirements

Before running the app, make sure you have:

- Python 3.9+
- A Google Gemini API key

## Setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run the App

Start the Streamlit app with:

```bash
streamlit run code.py
```

Then open the local URL shown in the terminal in your browser.

## How It Works

When a user submits a message, the app:

- stores the message in the session state,
- sends it to the Gemini model with a system instruction,
- keeps the conversation context using `previous_interaction_id`,
- displays the assistant response in the chat,
- saves the answer to the conversation history.
- If the API request fails, the app shows an error message instead of crashing.