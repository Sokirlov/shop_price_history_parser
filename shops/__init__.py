import os
import importlib
import inspect

# Поточна директорія (де знаходиться __init__.py)
current_dir = os.path.dirname(__file__)

# Динамічний імпорт усіх модулів у папці
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{__name__}.{filename[:-3]}"  # Ім'я модуля, наприклад, shops.Silpo
        module = importlib.import_module(module_name)

        # Ітерація по членах модуля та додавання класів у глобальні змінні
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Перевіряємо, що клас визначений у цьому модулі
            if obj.__module__ == module_name:
                globals()[name] = obj
