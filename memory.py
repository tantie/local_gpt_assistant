import json
import ast
import re
from config import MEMORY_FILE, PROJECT_ROOT, EXCLUDED_DIRS

CODE_FILES = {".py", ".php", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".swift", ".rs"}

def format_structure(structure, indent=0):
    result = ""
    for key, value in structure.items():
        result += " " * indent + f"{key}/\n" if isinstance(value, dict) else " " * indent + f"{key}\n"
        if isinstance(value, dict):
            result += format_structure(value, indent + 2)
    return result

def get_project_structure():
    structure = {}

    for p in PROJECT_ROOT.rglob("*"):
        if any(excl in p.parts for excl in EXCLUDED_DIRS):
            continue

        parts = list(p.relative_to(PROJECT_ROOT).parts)
        current = structure
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = "file" if p.is_file() else {}

    return structure

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}

    memory.setdefault("chats", {})
    memory.setdefault("files", {})
    memory.setdefault("structure", {})
    memory.setdefault("selected_files", {})

    return memory

def extract_definitions(file_content, file_extension):
    if file_extension == ".py":
        try:
            tree = ast.parse(file_content)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            return {"functions": functions, "classes": classes}
        except Exception:
            return {}

    regex_patterns = {
        ".php": [r"function (\w+)", r"class (\w+)"],
        ".js": [r"function (\w+)", r"class (\w+)"],
        ".ts": [r"function (\w+)", r"class (\w+)", r"interface (\w+)"],
        ".java": [r"public\s+\w+\s+(\w+)\(", r"class (\w+)"],
        ".cpp": [r"\w+\s+(\w+)\(.*?\)", r"class (\w+)"],
        ".c": [r"\w+\s+(\w+)\(.*?\)"],
        ".go": [r"func (\w+)", r"type (\w+) struct"],
        ".swift": [r"func (\w+)", r"class (\w+)", r"struct (\w+)"],
        ".rs": [r"fn (\w+)", r"struct (\w+)", r"impl (\w+)"]
    }

    functions, classes = [], []
    for pattern in regex_patterns.get(file_extension, []):
        matches = re.findall(pattern, file_content)
        if "class" in pattern:
            classes.extend(matches)
        else:
            functions.extend(matches)

    return {"functions": functions, "classes": classes}

def update_memory(chat_id=None):
    structure = get_project_structure()
    memory = load_memory()

    if chat_id:
        memory["chats"].setdefault(chat_id, [])
        memory["selected_files"].setdefault(chat_id, [])

    memory["structure"] = structure
    save_memory(memory)
