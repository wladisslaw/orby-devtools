from typing import Dict, Tuple
import json
from pathlib import Path
import shutil

from .master import TEMPLATES_DIR


class Templates:
    """
    Предоставляет интерфейс для работы с шаблонами.
    """

    @staticmethod
    def templates_list() -> Tuple[Dict[str, str], Exception | None]:
        """
        Возвращает список всех доступных шаблонов разработки.

        Returns:
            Кортеж, содержащий:
                Dict[str, str]: Словарь с информацией о шаблонах, где:
                    - key (str): Имя шаблона.
                    - value (str): Описание шаблона из manifest.json
                            (пустая строка, если manifest отсутствует или невалиден).
                Exception | None: Исключение, если возникла ошибка при чтении шаблонов, 
                            None если ошибок не было.
        """

        try:
            templates = {}
            
            for template_dir in TEMPLATES_DIR.iterdir():
                if template_dir.is_dir():
                    manifest_path = template_dir / "manifest.json"
                    template_info = ""

                    if manifest_path.exists():
                        try:
                            with open(manifest_path, 'r') as f:
                                manifest = json.load(f)
                                template_info = manifest.get("description", "")
                        except json.JSONDecodeError as e:
                            template_info = "Invalid manifest.json"
                    
                    templates[template_dir.name] = template_info
            
            return templates, None

        except Exception as e:
            return {}, e
    
    @staticmethod
    def savetemplate(name: str, path: str) -> Tuple[bool, Exception | None]:
        """
        Сохраняет новый шаблон.

        Args:
            name (str): Имя сохраняемого шаблона.
            path (str): Путь к папке, сохраняемой как шаблон.
        
        Returns:
            Кортеж, содержащий:
                bool: Статус выполнения.
                Exception | None: Исключение, если возникла ошибка при сохранении шаблона, 
                            None если ошибок не было.
        """

        try:
            exists_templates, exception = Templates.templates_list()
            if exception is not None:
                raise Exception(f"Problems with general files. Exception: {exception}") from exception
            
            if name in exists_templates.keys():
                raise Exception(f"Project with name '{name}' already exists.")
            
            _from = Path(path)
            manifest = _from / "manifest.json"
            if not manifest.exists():
                raise Exception(f"It is no `manifest.json` in '{_from}'")

            target_path = TEMPLATES_DIR / name
            shutil.copytree(_from, target_path)

        except Exception as e:
            return False, e