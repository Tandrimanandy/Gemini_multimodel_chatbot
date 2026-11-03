# Gemini Multimodal Chatbot

A text and image chatbot built with the official Google Gen AI Python SDK and a Streamlit web interface. Users can ask text questions or upload an image and ask Gemini to describe, explain, or analyze it, with conversation context preserved across turns.

[![Google Gen AI SDK](https://img.shields.io/badge/Google%20Gen%20AI%20SDK-Docs-4285F4?style=for-the-badge)](https://googleapis.github.io/python-genai/)
[![generate_content](https://img.shields.io/badge/generate__content-API%20Reference-34A853?style=for-the-badge)](https://ai.google.dev/api/generate-content)
[![Gemini API Keys](https://img.shields.io/badge/Gemini%20API-Get%20a%20Key-FBBC04?style=for-the-badge&labelColor=333333)](https://aistudio.google.com/app/apikey)
[![Streamlit](https://img.shields.io/badge/Streamlit-Docs-FF4B4B?style=for-the-badge)](https://docs.streamlit.io)
[![st.chat_input](https://img.shields.io/badge/st.chat__input-API%20Reference-FF4B4B?style=for-the-badge)](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)
[![st.file_uploader](https://img.shields.io/badge/st.file__uploader-API%20Reference-FF4B4B?style=for-the-badge)](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-Documentation-ECD53F?style=for-the-badge&labelColor=333333)](https://pypi.org/project/python-dotenv/)
[![Pillow](https://img.shields.io/badge/Pillow-Documentation-5A8F29?style=for-the-badge)](https://pillow.readthedocs.io)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [How It Works](#how-it-works)
- [Function Reference](#function-reference)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Security Notes](#security-notes)
- [References](#references)
- [License](#license)

---

## Overview

The project is organized into two files with clearly separated responsibilities:

- **Backend (`gemini_bot.py`)**: Loads the API key, creates the Gemini client, converts chat history into SDK content objects, encodes optional images, and returns the model response.
- **Frontend (`app.py`)**: Renders the chat interface, handles the image upload, maintains conversation state, and displays responses and errors.

The backend uses plain Python functions only and does not define custom classes, which keeps the code approachable for beginners.

---

## Features

- Text-based question answering using Gemini
- Image understanding: upload a PNG, JPG, JPEG, or WEBP image and ask questions about it
- Multi-turn conversation with recent text history passed as context
- Clear conversation control in the sidebar
- Secure API key handling through a local `.env` file
- Custom dark theme with a yellow and brown color palette, configured through Streamlit's theme settings
- Command-line test mode for the text backend, independent of the web interface

---

## Technology Stack

| Component | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| google-genai | Official Google Gen AI SDK for calling Gemini models |
| Streamlit | Web-based user interface |
| python-dotenv | Loads environment variables from the `.env` file |
| Pillow | Opens, converts, and encodes uploaded images |

---

## Project Structure

```text
gemini_multimodal_chatbot/
├── app.py               # Streamlit frontend
├── gemini_bot.py        # Gemini backend functions
├── requirements.txt     # Python dependencies
├── .env                 # Private API key (not committed)
├── .env.example         # Template for the .env file
├── .gitignore           # Excludes secrets and temporary files
├── .streamlit/
│   └── config.toml      # Streamlit theme configuration
└── README.md            # Project documentation
```

| File | Description |
|---|---|
| `app.py` | Builds the Streamlit interface, collects text and image input, and displays the conversation |
| `gemini_bot.py` | Contains all Gemini API logic, including client creation, conversation building, and response generation |
| `requirements.txt` | Lists the Python packages required by the project |
| `.env` | Stores the `GEMINI_API_KEY` value; must never be shared or committed |
| `.env.example` | Provides a placeholder template that can be safely committed |
| `.gitignore` | Prevents secrets, virtual environments, and cache files from entering version control |
| `.streamlit/config.toml` | Defines the dark theme colors and font for the Streamlit interface |

---

## Prerequisites

- Python 3.11 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- An active internet connection
- Terminal access (Windows PowerShell or Command Prompt, macOS Terminal, or Linux shell)

---

## Installation

### 1. Install uv

[uv](https://docs.astral.sh/uv/) is used to create the virtual environment and install dependencies.

```bash
pip install uv
```

### 2. Create the project folder and virtual environment

```bash
mkdir gemini_multimodal_chatbot
cd gemini_multimodal_chatbot
uv venv
```

### 3. Activate the virtual environment

Windows (PowerShell or Command Prompt):

```bash
.venv\Scripts\activate
```

macOS and Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## Configuration

### Set up the API key

1. Create a file named `.env` in the project root directory.
2. Add your Gemini API key using the following format, without quotation marks:

```env
GEMINI_API_KEY=your_actual_api_key
```

3. Save the file. Do not commit it to version control.

A template is provided in `.env.example`:

```env
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

### Recommended .gitignore

```gitignore
.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

### Changing the model

The model is defined in `gemini_bot.py`:

```python
MODEL_NAME = "gemini-2.5-flash"
```

If the model is unavailable for your API key, replace this value with a model listed in Google AI Studio.

---

## Running the Application

### Option 1: Command-line text test

This verifies that the backend and API key work correctly before launching the interface.

```bash
python gemini_bot.py
```

Type a question when prompted. The response is printed in the terminal.

### Option 2: Streamlit web interface

```bash
streamlit run app.py
```

Streamlit opens the application automatically in your browser. If it does not, navigate to:

```text
http://localhost:8501
```

---

## How It Works

1. The user enters a text message and, optionally, uploads an image in `app.py`.
2. `gemini_bot.py` loads `GEMINI_API_KEY` from the `.env` file using `python-dotenv`.
3. `create_gemini_client()` creates a client using the Google Gen AI SDK.
4. `build_conversation()` converts the previous text messages and the current prompt into Gemini content objects.
5. If an image is provided, `get_gemini_response()` converts it to RGB, encodes it as JPEG bytes, and attaches it to the latest user message.
6. The request is sent to the model through `client.models.generate_content()`.
7. The response text is returned to `app.py` and displayed in the chat window.
8. The conversation is stored in Streamlit session state for the duration of the browser session.

### Important behavior notes

- A text-only question sends text content only.
- An image question sends the text prompt together with the image bytes.
- Conversation history is kept in session state and is not stored permanently.
- Only recent text history is sent as context. Images from earlier turns are not resent.
- API usage, quotas, and pricing depend on your Google AI Studio project and current plan.

---

## Function Reference

### `gemini_bot.py`

| Function | Description |
|---|---|
| `get_api_key()` | Reads `GEMINI_API_KEY` from the environment and raises a clear error if it is missing |
| `create_gemini_client()` | Creates and returns a `genai.Client` instance using the validated API key |
| `build_conversation(prompt, chat_history)` | Converts stored messages into `types.Content` objects, mapping the assistant role to `model` |
| `get_gemini_response(prompt, image=None, chat_history=None)` | Validates input, builds the request, optionally attaches an image, calls the model, and returns the text |
| `test_text_chat()` | Command-line helper for testing the text chatbot |

### `app.py`

| Component | Description |
|---|---|
| `st.set_page_config()` | Sets the browser tab title, icon, and wide layout |
| `st.session_state` | Stores the conversation messages across reruns |
| `st.file_uploader()` | Accepts optional PNG, JPG, JPEG, or WEBP images |
| `st.chat_input()` | Provides the message input field at the bottom of the page |
| `st.chat_message()` | Displays user and assistant messages |
| `st.spinner()` | Shows a loading indicator while Gemini generates a response |
| `st.rerun()` | Refreshes the page after the conversation is cleared |

---

## Usage Examples

| Input type | Example prompt | Expected result |
|---|---|---|
| Text | Explain Python functions with a simple example | A beginner-friendly explanation with code |
| Text | What is machine learning? | A general conceptual explanation |
| Image | Upload a food photo and ask: What food is shown? | A description of the visible food |
| Image | Upload a flowchart and ask: Explain the steps | A walkthrough of the visible steps |
| Image | Upload a receipt and ask: What is the total? | The visible receipt information |
| Image | Upload a diagram and ask: Explain the components | An explanation of the visible components |
| Follow-up | Ask: Can you simplify that? | A response that uses the previous text context |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `GEMINI_API_KEY was not found` | Confirm that `.env` is in the same folder as `gemini_bot.py` and that the variable name is spelled exactly as shown |
| `ModuleNotFoundError` | Activate the virtual environment and run `uv pip install -r requirements.txt` |
| Invalid API key or permission error | Create or verify your key in Google AI Studio and check that it is copied without extra spaces or quotation marks |
| Unsupported image format | Use PNG, JPG, JPEG, or WEBP. Resize very large images before uploading |
| Model unavailable | Check the models accessible to your API key and update `MODEL_NAME` in `gemini_bot.py` |
| Streamlit command not found | Confirm that the virtual environment is activated before running `streamlit run app.py` |

---

## Limitations

- Conversation history is stored only in the current browser session and is lost when the page is refreshed or the server restarts.
- Images from earlier turns are not resent to the model; only the image attached to the current message is analyzed.
- Image analysis describes only what can reasonably be observed and may not be accurate for fine details, text in low-resolution images, or ambiguous content.
- The application does not implement rate limiting, authentication, or multi-user isolation and is intended for local learning and demonstration.

---

## Security Notes

- Never commit the `.env` file or share your API key publicly.
- If a key is accidentally exposed, revoke it immediately in Google AI Studio and create a new one.
- Keep `.env` listed in `.gitignore` before the first commit.

---

## References

- [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/)
- [Gemini API: Generate Content](https://ai.google.dev/api/generate-content)
- [Google AI Studio: API Keys](https://aistudio.google.com/app/apikey)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit: st.chat_input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)
- [Streamlit: st.file_uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Pillow Documentation](https://pillow.readthedocs.io)
- [uv Documentation](https://docs.astral.sh/uv/)

---

## License

This project is released under the MIT License. See the `LICENSE` file for details.
