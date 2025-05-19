from typing import Dict, Tuple
import json

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
                    template_info = {
                        "path": str(template_dir.absolute()),
                        "description": ""
                    }

                    if manifest_path.exists():
                        try:
                            with open(manifest_path, 'r') as f:
                                manifest = json.load(f)
                                template_info["description"] = manifest.get("description", "")
                        except json.JSONDecodeError as e:
                            template_info["description"] = "Invalid manifest.json"
                    
                    templates[template_dir.name] = template_info
            
            return templates, None

        except Exception as e:
            return {}, e