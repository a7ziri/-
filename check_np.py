import torch
import matplotlib.pyplot as plt

def visualize_schematic(tensor_file):
    """
    Визуализирует трехмерный тензор PyTorch, представляющий схему Minecraft.

    Параметры:
        tensor_file (str): Путь к файлу тензора.
    """
    # Загрузка тензора PyTorch
    blocks_tensor = torch.load(tensor_file)

    # Транспонирование тензора для изменения порядка осей
    blocks_tensor = blocks_tensor.permute(1, 2, 0)

    # Создание 3D-графика
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Получение индексов ненулевых элементов
    non_zero_indices = torch.nonzero(blocks_tensor > 0)

    # Разделение индексов на координаты
    x, y, z = non_zero_indices[:, 0], non_zero_indices[:, 1], non_zero_indices[:, 2]

    # Визуализация точек
    ax.scatter(x, y, z, c='b', marker='o')

    # Настройка осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Показ графика
    plt.show()

def extract_block_info(tensor_file):
    """
    Извлекает информацию о блоках из трехмерного тензора PyTorch.

    Параметры:
        tensor_file (str): Путь к файлу тензора.

    Возвращает:
        list: Список с информацией о блоках.
    """
    # Загрузка тензора PyTorch
    blocks_tensor = torch.load(tensor_file)

    # Транспонирование тензора для изменения порядка осей
    blocks_tensor = blocks_tensor.permute(1, 2, 0)

    # Получение индексов ненулевых элементов
    non_zero_indices = torch.nonzero(blocks_tensor > 0)

    # Извлечение информации о блоках
    block_info = []
    for index in non_zero_indices:
        x, y, z = index
        block_type = blocks_tensor[x, y, z]
        block_info.append((x.item(), y.item(), z.item(), block_type.item()))

    return block_info

# Пример использования
tensor_file = 'converted_schemes/[Small]_House.pt'
visualize_schematic(tensor_file)

block_info = extract_block_info(tensor_file)

# Вывод информации о блоках
for info in block_info:
    print(f"Координаты: ({info[0]}, {info[1]}, {info[2]}), Тип блока: {info[3]}")
