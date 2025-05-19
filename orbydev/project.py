from pathlib import Path
import shutil

TEMPLATES_DIR = Path(__file__).parent / "templates"

def create_project(name: str, template: str = "default"):
    """Generate a new project from a template."""
    target_dir = Path(name)
    template_dir = TEMPLATES_DIR / template
    
    if not template_dir.exists():
        raise ValueError(f"Template '{template}' not found!")
    
    shutil.copytree(template_dir, target_dir)
    # Дополнительные действия (например, подстановка имени в манифест)