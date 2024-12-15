import os
from PIL import Image
import ollama

def generate_text(instruction, file_path):
    result = ollama.generate(
        model='llava',
        prompt=instruction,
        images=[file_path],
        stream=False
    )['response']
    return result

def process_images(image_folder, text_folder, instruction):
    # Создаем основную папку для текстовых файлов, если она не существует
    os.makedirs(text_folder, exist_ok=True)

    for root, dirs, files in os.walk(image_folder):
        image_processed = False
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(root, file)
                description = generate_text(instruction, image_path)
                
                # Создаем текстовый файл с тем же именем, что и изображение, но в папке text
                relative_path = os.path.relpath(root, image_folder)
                text_subfolder = os.path.join(text_folder, relative_path)
                os.makedirs(text_subfolder, exist_ok=True)
                
                txt_file = os.path.join(text_subfolder, os.path.splitext(file)[0] + '.txt')
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(description)
                
                print(f"Обработано: {image_path}")
                print(f"Описание сохранено в: {txt_file}")
                
                image_processed = True
                break  # Обрабатываем только первое изображение в каждой папке
        
        if not image_processed:
            print(f"Изображений не найдено в: {root}")

# Основное выполнение
if __name__ == "__main__":
    image_folder = 'image'
    text_folder = 'text'
    instruction = """Just  build  this in  minecraft  help describe in  one  or  two  sentences the images fosucing  on it  main  details and  elements and  name  all  materials so that everyone can build according to this description, but be brief

     """
    process_images(image_folder, text_folder, instruction)
    print("Все изображения успешно обработаны!")