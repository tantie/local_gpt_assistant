import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# API-ключ OpenAI
OPENAI_API_KEY = "YOU_OPENAI_API_KEY"

# Расширения файлов, которые отслеживаются
CODE_EXTENSIONS = {".py", ".js", ".ts", ".html", ".css", ".json", ".md", ".php"}

# Исключённые папки
EXCLUDED_DIRS = {
    ".git", "venv", "__pycache__", ".idea", ".vscode", ".DS_Store", ".gpt_memory.json",  ".gpt_chat_memory.json", "sftp-config.json"}

# Пути внутри проекта
SCRIPT_PATH = Path(__file__).resolve()
GPT_SCRIPT_FOLDER = SCRIPT_PATH.parent
PROJECT_ROOT = GPT_SCRIPT_FOLDER.parent  

# Файл памяти (структура проекта + функции + классы)
MEMORY_FILE = PROJECT_ROOT / ".gpt_memory.json"
