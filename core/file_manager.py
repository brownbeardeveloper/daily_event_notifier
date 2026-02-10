from pathlib import Path
import json

def read_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError("File not found")
    
    with open(file_path, "r") as f:
        return json.load(f)

def write_json(file_path: Path, data: dict) -> None:
    if data == None:
        raise ValueError("Data cannot be None")
    
    with open(file_path, "w") as f:
        json.dump(data, f)