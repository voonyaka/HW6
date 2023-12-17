from pathlib import Path
import shutil
import zipfile
import sys

def normalize(name):
    name = name.lower()
    translit_table = str.maketrans("абвгдеёзийклмнопрстуфхъыэ", "abvgdeezijklmnoprstufh'ye")
    name = name.translate(translit_table)
    name = ''.join([char if char.isalnum() or char in ['.', '_'] else '_' for char in name])
    return name

def process_folder(folder_path):
    items = list(folder_path.iterdir())

    for item in items:
        if item.is_file():
            process_file(item, folder_path)
    
    if not any(folder_path.iterdir()):
        folder_path.rmdir()
        return
    
    for item in items:
        if item.is_dir() and item.name.lower() not in ['archives', 'videos', 'audio', 'documents', 'images', 'others']:
            process_folder(item)

        
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()

def process_file(file_path, target_path):
    file_extension = file_path.suffix.lower()[1:]
    normalized_name = normalize(file_path.stem)

    if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
        destination_folder = 'images'
    elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
        destination_folder = 'videos'
    elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
        destination_folder = 'documents'
    elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
        destination_folder = 'audio'
    elif file_extension in ['zip']:
        destination_folder = 'archives'
        extract_folder = target_path / 'archives' / normalized_name

        try:
            
            extract_folder.mkdir(parents=True, exist_ok=True)
            
            if file_extension == 'zip':
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
            
            file_path.unlink()
            
            for extracted_item in extract_folder.iterdir():
                destination_path = target_path / destination_folder / extracted_item.name
                extracted_item.rename(destination_path)
            
            extract_folder.rmdir()
        except Exception as e:
            print(f"Error extracting {file_path.name}: {e}")
        return
    else:
        destination_folder = 'others'
    
    (target_path / destination_folder).mkdir(parents=True, exist_ok=True)

    destination_path = target_path / destination_folder / file_path.name
    shutil.move(file_path, destination_path)
def main():
    
    if len(sys.argv) != 2:
        print("Usage: python <main.py> <folder_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    target_path = Path(folder_path)

    for folder in ['images', 'videos', 'documents', 'audio', 'archives', 'others']:
        (target_path / folder).mkdir(parents=True, exist_ok=True)
    process_folder(target_path)

main()

