import os
import shutil

def compare_and_remove_folders(text_folder, converted_schemes_folder):
    # Получаем список папок в папке converted_schemes
    converted_files = [f for f in os.listdir(converted_schemes_folder) if os.path.isfile(os.path.join(converted_schemes_folder, f))]
    
    # Получаем список папок в папке text
    text_folders = [f for f in os.listdir(text_folder) if os.path.isdir(os.path.join(text_folder, f))]
    
    for folder in text_folders:
        # Проверяем, есть ли файл с таким же названием в папке converted_schemes
        if f"{folder}.pt" not in converted_files:
            # Удаляем папку, если файл не найден
            shutil.rmtree(os.path.join(text_folder, folder))
            print(f"Удалена папка: {folder}")

# Пример использования
compare_and_remove_folders('text', 'converted_schemes')