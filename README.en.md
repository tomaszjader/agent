# Google ADK-based Agent

A simple, configurable AI agent built entirely using the `google-adk` library. The agent can use defined tools to answer questions and perform tasks in natural language.

## Main Features

- **Google ADK-based Architecture**: Uses the official `google-adk` library for planning, session management, and tool calling.
- **Tools**: The agent has access to the following tools:
  - `tell_time`: Provides the current date and time.
  - `create_note`: Creates notes on the computer.
  - `sum_numbers`: Sums a list of numbers.
  - `google_search`: Searches for information on the internet (built-in ADK tool).
  - `propose_caption`: Suggests a caption for an Instagram post.
  - `publish_post`: Publishes a post on Instagram.
- **Gemini Model**: Powered by models from the Google Gemini family (e.g., `gemini-2.5-flash`).
- **Interactive and Single-shot Mode**: It can be run in a loop for a conversation or to execute a single instruction.

## Requirements

- Python 3.9+
- Google API Key (Google AI Studio)

## Installation

1.  **Clone the repository or download the files.**

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    python -m pip install -r requirements.txt
    ```

## Configuration

1.  **Copy the `.env.example` file to a new file named `.env`:**
    ```bash
    cp .env.example .env
    ```

2.  **Open the `.env` file and paste your Google API key:**
    ```env
    GOOGLE_API_KEY="YourGoogleApiKey"
    ```

3.  **(Optional) Change the Gemini model or session IDs:**
    You can change the default `gemini-2.5-flash` model to another compatible model from the Gemini family. You can also customize the session IDs if needed.

## Usage

The agent can be run in two ways:

### 1. Interactive Mode (in the console)

Run the `agent.py` script without any arguments to start a conversation with the agent in the terminal. Type `exit` to end.

```bash
python agent.py
```

**Example:**
```
> What time is it now?
2023-10-27 10:30:00

> Create a note named 'list.txt' with the text: buy milk
The note has been saved to 'list.txt'.

> What is the capital of France?
The capital of France is Paris.
```

### 2. Single-shot Mode (in the console)

Use the `-i` or `--instruction` flag to pass a single command to the `agent.py` script. The agent will perform the task and exit.

```bash
python agent.py --instruction "Sum the numbers 10, 25, and 7.5"
```

**Response:**
```
Sum: 42.5
```

### 3. Telegram Bot

The agent can also be run as a Telegram bot, allowing you to interact with it via messages.

**Telegram Bot Configuration:**

1.  **Create a bot and get a token:**
    -   Talk to [@BotFather](https://t.me/BotFather) on Telegram.
    -   Use the `/newbot` command to create a new bot.
    -   Follow the instructions, and you will receive a token at the end.

2.  **Add the token to the `.env` file:**
    Open the `.env` file and add a new `TELEGRAM_BOT_TOKEN` variable:
    ```env
    GOOGLE_API_KEY="YourGoogleApiKey"
    TELEGRAM_BOT_TOKEN="YourTelegramBotToken"
    ```

**Running the Bot:**

To run the bot, execute the following command:

```bash
python bot.py
```

The bot will run in the background and respond to messages sent on Telegram. You can send it both text commands and photos.

## Project Structure

```
agent/
│
├── .env.example      # Example configuration of environment variables
├── .gitignore        # Files ignored by Git
├── agent.py          # Main agent script (console mode)
├── bot.py            # Script to run the Telegram bot
├── requirements.txt  # Project dependencies
├── README.md         # This file
│
└───tools/            # Directory with tools
    ├── __init__.py
    ├── create_google_keep_note.py
    ├── create_note.py
    ├── prepare_instagram_post.py
    ├── publish_instagram_post.py
    ├── sum_numbers.py
    └── tell_time.py
```