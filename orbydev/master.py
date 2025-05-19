from pathlib import Path
import json

MAIN_DIR = Path(__file__).parent
TEMPLATES_DIR = MAIN_DIR / "templates"

DEVTOOLS_DATA = Path.home() / ".orby" / "devtools" 
DEVTOOLS_DATA.mkdir(exist_ok=True, parents=True)

PROJECTS_DB = DEVTOOLS_DATA / "projects.json"
if not PROJECTS_DB.exists():
    PROJECTS_DB.write_text("{}", "utf-8")

TEMPLATES_DB = DEVTOOLS_DATA / "templates.json"
if not TEMPLATES_DB.exists():
    TEMPLATES_DB.write_text(json.dumps(
        {
            "templates" : ["default"]
        },
        ensure_ascii=False,
        indent=4
    ), "utf-8")