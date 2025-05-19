import zipfile
import json
from pathlib import Path

def build_project(path: str) -> str:
    """Pack the project into a .orby file."""
    project_dir = Path(path)
    manifest = json.loads((project_dir / "manifest.json").read_text())
    
    # Проверка манифеста
    if "name" not in manifest:
        raise ValueError("Manifest must contain 'name' field!")
    
    # Сборка архива
    orby_file = f"{manifest['name']}.orby"
    with zipfile.ZipFile(orby_file, "w") as zipf:
        for file in project_dir.glob("**/*"):
            if file.is_file():
                zipf.write(file, file.relative_to(project_dir))
    
    return orby_file