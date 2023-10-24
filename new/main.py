import os
import sys


# Получите путь к текущей директории (где находится ваш exe файл)
exe_directory = os.path.dirname(sys.executable)
# Затем используйте относительные пути относительно текущей директории
file_path = os.path.join(exe_directory, "input.txt")
print(exe_directory)
print(file_path)
try:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        print("Содержимое файла:")
        print(file_contents)
except FileNotFoundError:
    print("Файл не найден. Убедитесь, что путь к файлу указан правильно.")
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")

input("Нажмите Enter для завершения...")