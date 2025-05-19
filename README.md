# Orby DevTools

**Orby DevTools** — инструмент для разработки изолированных Python-приложений под платформу Orby. Позволяет создавать, валидировать и собирать приложения в защищённый `.orby` формат для запуска через Orby-совместимые среды.

## Возможности

- Генерация проектов из шаблонов  
- Сборка в `.orby` архив с манифестом  
- Валидация структуры проекта  
- Поддержка кастомных разрешений  
- Автогенерация зависимостей  

## Быстрый старт

### Установка
```bash
pip install orby-devtools
```

### Базовое использование
1. Создать проект:
```bash
orbydev new myapp --template=default
```
2. Собрать в `.orby`:
```bash
orbydev build myapp
```

## Команды CLI

| Команда | Описание |
|---------|----------|
| `new <name> <path> [--template=...]` | Создать проект в указанной директории |
| `build <path> <save_at>` | Собрать проект из директории в `.orby` |
| `savetemplate <name> <path>` | Сохранить проект как шаблон |
| `templates` | Список всех шаблонов |
| `deletetemplate <name>` | Удалить шаблон |

## Структура проекта
```
myapp/
├── main.py              # Точка входа
├── manifest.json        # Конфигурация
└── requirements.txt     # Зависимости
```

## Пример `manifest.json`
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "My Orby app",
  "permissions": {
    "fs": ["read", "/data/"],
    "net": ["api.example.com"]
  },
  "entry_point": "main.py"
}
```

## Полезное
- [Баг-трекер](https://github.com/wladisslaw/orby-devtools/issues)
- Совместимость: Python 3.10+
- Статус: Beta