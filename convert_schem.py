from nbtlib import nbt
import numpy as np
import torch
import os 

def schematic_to_numpy(file_path):

        schematic = nbt.load(file_path)
        
        # Выводим структуру NBT для отладки
        print("NBT структура:", schematic)
        
        # Получаем размеры более безопасным способом
        width = int(schematic.get('Width', 0))
        height = int(schematic.get('Height', 0))
        length = int(schematic.get('Length', 0))
        
        print(f"Размеры: {width}x{height}x{length}")
        
        # Получаем блоки
        blocks = schematic.get('Blocks', [])
        
        # Пропускаем очень большие массивы
        if len(blocks) > 50_000:  # Пример порога, можно изменить
            print(f"Пропущен файл {file_path}: слишком большой массив блоков.")
            return None
        
        # Преобразуем в numpy массив
        blocks = np.array(blocks, dtype=np.uint8)
        
        # Проверяем размер
        if len(blocks) != width * height * length:
            raise ValueError(f"Неверный размер массива блоков: {len(blocks)} != {width * height * length}")
        
        # Преобразуем в 3D массив
        blocks = blocks.reshape((height, length, width))

        return blocks

def remove_air(blocks):
    # Находим непустые блоки
    non_air_mask = blocks != 0  # 0 обычно воздух
    
    # Находим границы непустых блоков
    x_indices, y_indices, z_indices = np.where(non_air_mask)
    
    if len(x_indices) == 0:
        return blocks
        
    # Обрезаем массив по минимальным размерам
    return blocks[min(x_indices):max(x_indices)+1,
                 min(y_indices):max(y_indices)+1,
                 min(z_indices):max(z_indices)+1]
# Пример использования
def process_all_schematics(input_folder, output_folder):
    """
    Обрабатывает все .schematic файлы в указанной папке и сохраняет результаты.

    Параметры:
        input_folder (str): Путь к папке с .schematic файлами.
        output_folder (str): Путь к папке для сохранения результатов.
    """
    # Создаем выходную папку, если она не существует
    os.makedirs(output_folder, exist_ok=True)

    # Перебираем все файлы в input_folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.schematic'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pt")

            try:
                # Конвертируем схему в NumPy массив
                blocks_array = schematic_to_numpy(input_path)
                
                # Пропускаем, если массив не был создан
                if blocks_array is None:
                    continue

                # Очищаем массив от воздуха
                cleaned_blocks = remove_air(blocks_array)

                # Преобразуем в тензор PyTorch
                torch_tensor = torch.tensor(cleaned_blocks)

                # Сохраняем тензор PyTorch
                torch.save(torch_tensor, output_path)
                print(f"Обработан файл: {filename}")
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {str(e)}")

# Пример использования
if __name__ == "__main__":
    input_folder = 'schemes'  # Папка с .schematic файлами
    output_folder = 'converted_schemes'  # Папка для сохранения результатов
    process_all_schematics(input_folder, output_folder)
