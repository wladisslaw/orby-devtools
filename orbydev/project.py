from pathlib import Path
import shutil
import json
import zipfile

from .master import TEMPLATES_DIR


class Projects:
    """
    Предоставляет интерфейс для работы с проектами.
    """

    @staticmethod
    def new(name: str, path: str = "", template: str = "default") -> tuple[bool, Exception | None]:
        """
        Создаёт новый Orby проект и возвращает код выполнения.

        Args:
            name (str): Имя создаваемого проекта.
            path (str): Конечная дирректория проекта. Если не указать, будет создана дирректория с именем проекта.
            template (str, optional): Используемый шаблон. По умолчанию - `"default"`.
        
        Returns:
            status_code (bool): Статус выполнения.
            exception (Exception | None): Ошибка, вызванная во время выполнения. Если ошибок не было вызвано, то `None`.
        """

        try:
            target_dir = Path(path) if path != ""  else Path(name)
            template_dir = TEMPLATES_DIR / template

            if not template_dir.exists():
                raise ValueError(f"Template '{template}' not found!")
            
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)

            manifest_text = (target_dir / "manifest.json").read_text("utf-8")
            manifest_json = json.loads(manifest_text)
            manifest_json["name"] = name
            manifest_text = json.dumps(manifest_json, ensure_ascii=False, indent=4)
            (target_dir / "manifest.json").write_text(manifest_text, "utf-8")

            return True, None
        except Exception as e:
            return False, e
    
    @staticmethod
    def build(path: str, save_at: str = "") -> tuple[bool, Exception | None]:
        """
        Собирает проект в конечное .orby приложение.

        Args:
            path (str): Путь к папке собираемого проекта.
            save_at (str, optional): Где сохранять файл. Если не указать, будет сохранено в текущей дирректории.
        
        Returns:
            status_code (bool): Статус выполнения.
            exception (Exception | None): Ошибка, вызванная во время выполнения. Если ошибок не было вызвано, то `None`.
        """

        try:
            project_dir = Path(path)
            manifest = json.loads((project_dir / "manifest.json").read_text())

            if "name" not in manifest:
                raise ValueError("Manifest must contain 'name' field!")
            
            save_path = Path(save_at if save_at != "" else ".").absolute() / f"{manifest['name']}.orby"
            with zipfile.ZipFile(save_path, "w") as zipf:
                for file in project_dir.glob("**/*"):
                    if file.is_file():
                        zipf.write(file, file.relative_to(project_dir))
            
            return True, None
        except Exception as e:
            return False, e