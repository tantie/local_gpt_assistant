# Local GPT Chat Assistant

A simple web interface for interacting with OpenAI GPT, supporting chats, file uploads, and code analysis.

📂 Integration with Other Projects

This script is designed to be added as a folder to your existing project, allowing you to interact with GPT without the need for a separate repository or file uploads.

## 🚀 Features
- 📂 Manage chats (create, delete, save history)
- 💬 Send messages to GPT-4
- 📁 Select project files for analysis
- ⚡ Preset prompts (bug detection, code optimization, etc.)
- 🏗 Automatic project structure loading

## 🔧 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tantie/local_gpt_assistant/gpt-chat-assistant.git
   cd gpt-chat-assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-api-key
   ```
4. Run the server:
   ```bash
   uvicorn assistant:app --reload
   ```

## 🖥 Usage
1. Open `http://127.0.0.1:8000/` in your browser.
2. Create a new chat and start interacting with GPT.
3. Select project files for analysis.
4. Use preset prompts for code assistance.
