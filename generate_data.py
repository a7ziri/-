import os
import numpy as np
import pandas as pd
import  torch  
# Пути к папкам с данными
text_dir = 'text'
array_dir = 'converted_schemes'

# Функция для загрузки текстовых описаний
def load_texts(text_dir):
    texts = {}
    for root, _, files in os.walk(text_dir):
        print(f"Проверка директории: {root}")  # Отладочный вывод
        for filename in files:
            if filename.endswith('.txt'):
                print(f"Найден текстовый файл: {filename}")  # Отладочный вывод
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                    texts[filename] = file.read().strip()
    return texts

# Функция для загрузки 3D массивов
def load_arrays(array_dir):
    arrays = {}
    for root, _, files in os.walk(array_dir):
        print(f"Проверка директории: {root}")  # Отладочный вывод
        for filename in files:
            if filename.endswith('.pt'):
                print(f"Найден файл массива: {filename}")  # Отладочный вывод
                arrays[filename] = torch.load(os.path.join(root, filename)).numpy()  # Преобразование тензора в numpy массив
    return arrays

# Загрузка данных
texts = load_texts(text_dir)
arrays = load_arrays(array_dir)

# Отладочный вывод
print("Загруженные текстовые файлы:", list(texts.keys()))
print("Загруженные 3D массивы:", list(arrays.keys()))

# Создание датасета
dataset = []
text_filenames = sorted(texts.keys())
array_filenames = sorted(arrays.keys())

for text_filename, array_filename in zip(text_filenames, array_filenames):
    # Извлечение информации о блоках
    block_info = []
    non_zero_indices = np.argwhere(arrays[array_filename] > 0)  # Используем numpy массив
    for index in non_zero_indices:
        x, y, z = index
        block_type = arrays[array_filename][x, y, z]
        block_info.append((x, y, z, block_type))
    
    # Преобразование информации о блоках в строку
    block_info_str = str(block_info)
    dataset.append((texts[text_filename], block_info_str))

# Сохранение в CSV файл
df = pd.DataFrame(dataset, columns=['Description', 'Block Info'])
df.to_csv('dataset.csv', index=False)

# Пример доступа к данным
for description, block_info in dataset[:5]:  # Вывод первых 5 пар
    print("Описание:", description)
    print("Информация о блоках:", block_info)  # Теперь это строка с информацией о блоках
