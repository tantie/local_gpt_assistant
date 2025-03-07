import json
from fastapi import APIRouter, Form, Query
from fastapi.responses import JSONResponse
from config import PROJECT_ROOT

CHAT_MEMORY_FILE = PROJECT_ROOT / ".gpt_chat_memory.json"
MAX_CHAT_HISTORY = 15  # Количество последних сообщений, передаваемых в GPT

router = APIRouter()

def load_chat_memory():
    """Загружает сохранённые чаты из файла."""
    if CHAT_MEMORY_FILE.exists():
        with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"chats": {}}

def save_chat_memory(memory):
    """Сохраняет чаты в файл."""
    with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

@router.get("/get-chats")
async def get_chats():
    """Возвращает список сохранённых чатов."""
    memory = load_chat_memory()
    return JSONResponse(content={"chats": list(memory["chats"].keys())})

@router.get("/get-chat-history")
async def get_chat_history(chat_id: str = Query(...)):
    """Возвращает историю сообщений чата."""
    memory = load_chat_memory()
    history = memory["chats"].get(chat_id, [])
    return JSONResponse(content={"history": history})

@router.post("/create-chat")
async def create_chat(chat_id: str = Form("")):
    """Создаёт новый чат."""
    memory = load_chat_memory()
    if chat_id and chat_id not in memory["chats"]:
        memory["chats"][chat_id] = []
        save_chat_memory(memory)
    return JSONResponse(content={"status": "Chat created", "chat_id": chat_id})

@router.post("/delete-chat")
async def delete_chat(chat_id: str = Form("")):
    """Удаляет чат."""
    memory = load_chat_memory()
    if chat_id in memory["chats"]:
        del memory["chats"][chat_id]
        save_chat_memory(memory)
    return JSONResponse(content={"status": "Chat deleted", "chat_id": chat_id})

def get_chat(chat_id):
    """Загружает историю определённого чата."""
    memory = load_chat_memory()
    return memory["chats"].get(chat_id, [])

def get_chat_list():
    """Возвращает список всех чатов."""
    memory = load_chat_memory()
    return list(memory["chats"].keys())

def save_message(chat_id, role, message):
    """Сохраняет новое сообщение в чате."""
    memory = load_chat_memory()
    if chat_id not in memory["chats"]:
        memory["chats"][chat_id] = []
    memory["chats"][chat_id].append({"role": role, "content": message})
    save_chat_memory(memory)

def trim_chat_history(chat_id):
    """Сокращает историю чата, оставляя только важные сообщения."""
    memory = load_chat_memory()
    chat_history = memory["chats"].get(chat_id, [])

    if len(chat_history) > MAX_CHAT_HISTORY:
        important_messages = [msg for msg in chat_history if msg.get("important", False)]
        trimmed_history = important_messages + chat_history[-MAX_CHAT_HISTORY:]
        memory["chats"][chat_id] = trimmed_history
        save_chat_memory(memory)
        return trimmed_history

    return chat_history
