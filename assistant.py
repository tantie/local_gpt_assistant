from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from chat import router as chat_router
from chat_memory import router as chat_memory_router
from memory import get_project_structure, load_memory, save_memory, update_memory
from config import PROJECT_ROOT

app = FastAPI()
app.include_router(chat_router)
app.include_router(chat_memory_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get-structure")
async def get_structure():
    structure = get_project_structure()
    return JSONResponse(content={"structure": structure})  

@app.get("/get-chats")
async def get_chats():
    memory = load_memory()
    return JSONResponse(content={"chats": list(memory.get("chats", {}).keys())})

@app.get("/get-chat-history")
async def get_chat_history(chat_id: str):
    memory = load_memory()
    history = memory.get("chats", {}).get(chat_id, [])
    return JSONResponse(content={"history": history})

@app.post("/create-chat")
async def create_chat(chat_id: str = Form("")):
    memory = load_memory()
    if chat_id and chat_id not in memory["chats"]:
        memory["chats"][chat_id] = []
        memory.setdefault("selected_files", {})[chat_id] = []
        save_memory(memory)

    return JSONResponse(content={"status": "Chat created", "chat_id": chat_id})

@app.post("/delete-chat")
async def delete_chat(chat_id: str = Form("")):
    memory = load_memory()
    if chat_id in memory["chats"]:
        del memory["chats"][chat_id]

        if "selected_files" in memory and chat_id in memory["selected_files"]:
            del memory["selected_files"][chat_id]

        save_memory(memory)

    return JSONResponse(content={"status": "Chat deleted", "chat_id": chat_id})

@app.post("/select-files")
async def select_files(request: Request):
    data = await request.json()
    selected_files = data.get("files", [])
    chat_id = data.get("chat_id", None)

    if not chat_id or not isinstance(selected_files, list):
        return JSONResponse(content={"error": "Invalid request"}, status_code=400)

    memory = load_memory()

    memory.setdefault("selected_files", {})[chat_id] = selected_files

    save_memory(memory)

    return JSONResponse(content={"selected_files": selected_files})

@app.get("/get-files-for-chat")
async def get_files_for_chat(chat_id: str):
    memory = load_memory()
    selected_files = memory.get("selected_files", {}).get(chat_id, [])
    return JSONResponse(content={"files": selected_files})

@app.get("/get-gpt-data")
async def get_gpt_data():
    memory = load_memory()
    structure = "\n".join(memory.get("structure", []))
    selected_files = memory.get("selected_files", {})

    file_contents = []
    for chat_id, files in selected_files.items():
        for file in files:
            try:
                with open(PROJECT_ROOT / file, "r", encoding="utf-8") as f:
                    file_contents.append(f"\n=== {file} ===\n{f.read()}")
            except Exception as e:
                print(f"Ошибка чтения {file}: {e}")

    full_context = f"📂 Структура проекта:\n{structure}\n\n📄 Выбранные файлы:\n{''.join(file_contents)}"

    return JSONResponse(content={"content": full_context})

@app.get("/")
async def index():
    try:
        with open("templates/index.html", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return JSONResponse(content={"error": "index.html не найден"}, status_code=404)