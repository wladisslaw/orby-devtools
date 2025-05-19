from pathlib import Path
from typing import Dict, Tuple
import shutil
import json
import zipfile

from .master import TEMPLATES_DIR, PROJECTS_DB


class Projects:
    """
    Предоставляет интерфейс для работы с проектами.

    Methods:
        new (name, path, template): Создаёт новый Orby проект и возвращает код выполнения.
        build (path, save_at): Собирает проект в конечное .orby приложение.
        projects_list (): Возвращает список всех созданных через `orby-devtools` проектов.
        remove_project (name, remove_dir): Удаляет проект из списка проектов `orby-devtools`.
    """

    @staticmethod
    def new(name: str, path: str = "", template: str = "default") -> Tuple[bool, Exception | None]:
        """
        Создаёт новый Orby проект и возвращает код выполнения.

        Args:
            name (str): Имя создаваемого проекта.
            path (str): Конечная дирректория проекта. Если не указать, будет создана дирректория с именем проекта.
            template (str, optional): Используемый шаблон. По умолчанию - `"default"`.
        
        Returns:
            Кортеж, содержащий:
                bool: Статус выполнения.
                Exception | None: Исключение, если возникла ошибка при создании проекта, 
                            None если ошибок не было.
        """

        try:
            target_dir = Path(path) if path != ""  else Path(name)
            template_dir = TEMPLATES_DIR / template

            if not template_dir.exists():
                raise ValueError(f"Template '{template}' not found!")
            
            exists_projects, e = Projects.projects_list()

            if e is not None:
                raise Exception(f"Problems with general files. Exception: {e}") from e
            
            if name in exists_projects.keys():
                raise Exception(f"Project with name '{name}' already exists. Project path - '{exists_projects[name]['path']}'")
            
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)

            manifest_text = (target_dir / "manifest.json").read_text("utf-8")
            manifest_json = json.loads(manifest_text)
            manifest_json["name"] = name
            manifest_text = json.dumps(manifest_json, ensure_ascii=False, indent=4)
            (target_dir / "manifest.json").write_text(manifest_text, "utf-8")

            projects = json.loads(PROJECTS_DB.read_text("utf-8"))
            projects[name] = {"path": str(target_dir.absolute()), "template": template}

            PROJECTS_DB.write_text(json.dumps(projects, indent=4, ensure_ascii=False), "utf-8")

            return True, None
        except Exception as e:
            return False, e
    
    @staticmethod
    def build(path: str, save_at: str = "") -> Tuple[bool, Exception | None]:
        """
        Собирает проект в конечное .orby приложение.

        Args:
            path (str): Путь к папке собираемого проекта.
            save_at (str, optional): Где сохранять файл. Если не указать, будет сохранено в текущей дирректории.
        
        Returns:
            Кортеж, содержащий:
                bool: Статус выполнения.
                Exception | None: Исключение, если возникла ошибка при сборке проекта, 
                            None если ошибок не было.
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
    
    @staticmethod
    def projects_list() -> Tuple[Dict[str, dict], Exception | None]:
        """
        Возвращает список всех созданных через `orby-devtools` проектов.
    
        Returns:
            Кортеж, содержащий:
                Dict[str, dict]: Словарь с информацией о проектах, где:
                    - key (str): Имя проекта.
                    - value (dict): Информация о проекте.
                Exception | None: Исключение, если возникла ошибка при чтении проектов, 
                            None если ошибок не было.
        """
        try:
            return json.loads(PROJECTS_DB.read_text("utf-8")), None
        except Exception as e:
            return {}, e
    
    @staticmethod
    def remove_project(name: str, remove_dir: bool = False) -> Tuple[bool, Exception | None]:
        """
        Удаляет проект из списка проектов `orby-devtools`.

        Args:
            name (str): Имя удаляемого проекта.
            remove_dir (bool, optional): Удалять ли папку, где хранится проект. По умолчанию - `False`.

        Returns:
            Кортеж, содержащий:
                bool: Статус выполнения.
                Exception | None: Исключение, если возникла ошибка при удалении проекта, 
                            None если ошибок не было.
        """

        try:
            projects, e = Projects.projects_list()

            if e is not None:
                raise Exception(f"Problems with general files. Exception: {e}") from e
            if name not in projects.keys():
                raise Exception(f"Project with name '{name}' does not exists.")
            
            project_data = projects[name]
            
            if remove_dir:
                shutil.rmtree(project_data["path"])
            
            projects.pop(name, None)
            PROJECTS_DB.write_text(json.dumps(projects, indent=4, ensure_ascii=False), "utf-8")

            return True, None

        except Exception as e:
            return False, e