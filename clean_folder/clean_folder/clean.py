import re
import os
import shutil
import zipfile
import tarfile
from pathlib import Path

# Отримуємо шлях до поточного файлу
current_file_path = os.path.abspath(__file__)

# Отримуємо шлях до каталогу, що містить поточний файл
current_directory_path = os.path.dirname(current_file_path)

folder_path = current_directory_path
archives = folder_path + "\\archives"

# folder_path = Path(input("Enter your trash box path"))
# folder_path = Path('c:/Users/Илья/Desktop/Курсы/PythonCore')
# archives = Path('c:/Users/Илья/Desktop/Курсы/PythonCore/archives')
    
def normalize(name):
    
    CYRILLIC = ("а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м","н", "о", "п", "р", "с", "т", "у",
                    "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "є", "і", "ї", "ґ", "+", "-", "%", "$", ";", "№", "#", "@", "!", "^", "&", "(", ")", "=", ",", "[", "]", "{", "}", "`", "~")
    LATINA = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")

    TRANS = {}
    for c, l in zip(CYRILLIC, LATINA):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        
    return name.translate(TRANS)

def rename_files(folder_path):
    for r, d, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(r, file)
            new_file_name = normalize(file)
            new_file_path = os.path.join(r, new_file_name)
            os.rename(file_path, new_file_path)

# Створюємо словник, де ключ - це розширення файлу, а значення - це назва папки, де потрібно зберегти цей файл
file_extensions = {
    '.txt': 'documents',
    '.doc': 'documents',
    '.docx': 'documents',
    '.xlsx': 'documents',
    '.pdf': 'documents',
    '.pptx': 'documents',
    '.jpg': 'images',
    '.jpeg': 'images',
    '.png': 'images',
    '.svg': 'images',
    '.avi': 'video',
    '.mp4': 'video',
    '.mov': 'video',
    '.mkv': 'video',
    '.mp3': 'audio',
    '.ogg': 'audio',
    '.wav': 'audio',
    '.amr': 'audio',
    '.zip': 'archives',
    '.gz': 'archives',
    '.tar': 'archives',
    
}

def sort_files(folder_path, file_extensions):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            if filename not in ["video", "audio", "archives", "images", "documents"]:
                # Якщо файл - це папка, викликаємо функцію sort_files() рекурсивно для цієї папки
                sort_files(file_path, file_extensions)
        else:
            # Якщо файл - це файл, сортуємо його за розширенням
            file_extension = os.path.splitext(filename)[1]
            if file_extension in file_extensions:
                # Якщо розширення файлу є в словнику, переміщуємо файл до відповідної папки
                destination_folder = file_extensions[file_extension]
                if not os.path.exists(destination_folder):
                    # Якщо папка не існує, створюємо її
                    os.makedirs(destination_folder)
                destination_path = os.path.join(destination_folder, filename)
                shutil.move(file_path, destination_path)

def delete_empty_folders(path):
    # Рекурсивна функція для видалення порожніх папок
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path):
            if folder_name not in ["video", "audio", "archives", "images", "documents"]:
                delete_empty_folders(folder_path)
                # Видаляємо папку, якщо вона порожня
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)

def extract_archives(folder_path):
    # Створюємо список розширень архівів, які треба розпакувати
    archive_extensions = [".zip", ".ogg", ".tar"]

    # Ітеруємося по усіх файлах в папці "archives"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Перевіряємо, чи є це архів з розширенням, яке треба розпакувати
        if os.path.isfile(file_path) and any(file_name.endswith(ext) for ext in archive_extensions):
            # Створюємо папку з іменем архіву
            archive_folder = os.path.join(folder_path, os.path.splitext(file_name)[0])
            os.makedirs(archive_folder, exist_ok=True)

            # Розпаковуємо архів
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(archive_folder)
            elif file_name.endswith(".tar"):
                with tarfile.open(file_path, "r") as tar_ref:
                    tar_ref.extractall(archive_folder)
            elif file_name.endswith(".ogg"):
                shutil.unpack_archive(file_path, archive_folder)

rename_files(folder_path)
sort_files(folder_path, file_extensions)
delete_empty_folders(folder_path)
extract_archives(archives)