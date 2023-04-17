from sys import argv
from pathlib import Path
import shutil
import os

EXTENS = {
    "images": ['png', 'jpg', 'jpeg', 'svg'],
    "videos": ['avi', 'mp4', 'mov', 'mkv'],
    "documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'csv'],
    "audio": ['mp3', 'ogg', 'wav', 'amr'],
    "archives": ['zip', 'gz', 'tar'],
    "unknown": [] 
}
for key, value in EXTENS.items():
    if key != 'unknown':
        EXTENS['unknown'].extend(value)

def normalize(string):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    result = zip(CYRILLIC_SYMBOLS, TRANSLATION)    
    for el in list(result):
        TRANS[ord(el[0].lower())] = el[1].lower()
        TRANS[ord(el[0].upper())] = el[1].upper()
        
    def translate(name):
        return name.translate(TRANS)

    def remove_symbols(name):
        for char in name:
                if ord(char) >= 65 and ord(char) <= 90 or ord(char) >= 97 and ord(char) <= 122 or ord(char) >= 48 and ord(char) <= 57:
                    pass
                else:
                    name = name.replace(char, '_')
        return name
    return remove_symbols(translate(string))

def recursive_analyze(path, folders=[], files=[]):
    """Recursive search folders & files and rename folders and files for validation in argument path"""
    if path.is_dir():
        current_dir = Path(path).parent
        current_folder_name = Path(path).name
        new_name = f'{current_dir}/{normalize(current_folder_name)}'
        
        shutil.move(path, new_name)
        folders.append(new_name)
        
        for item in Path(new_name).iterdir():
            recursive_analyze(item)
    else:
        current_dir = Path(path).parent
        current_file_name = Path(path).stem
        current_suffix = Path(path).suffix
        new_name = f'{current_dir}/{normalize(current_file_name)}{current_suffix}'
        
        shutil.move(path, new_name)
        files.append(new_name)
        
    return folders, files

def rename_same_filename(paths_list: list):
    """Rename same filenames in directories"""
    count_name = {}

    for i, item in enumerate(paths_list):
        if Path(item).name not in count_name:
            count_name[str(Path(item).name)] = 1
        else:
            count_name[str(Path(item).name)] += 1
            old_file_name = Path(item)
            new_file_name = old_file_name.with_name(str(count_name[str(Path(item).name)]) + '_' + old_file_name.name)
            shutil.move(old_file_name, new_file_name)
            paths_list[i] = str(new_file_name)

    return paths_list

def make_structure(path_list: list, data) -> dict:
    files_collection = {}

    for element in path_list:
        for key, value in data.items():
            files_collection[key] = {}
            files_collection[key]['files'] = []

    for element in path_list:
        current_element_suffix = Path(element).suffix
        
        for key, value in data.items():
            if key != 'unknown' and current_element_suffix[1:] in value:
                files_collection[key]['files'].append(element)
            
            if key == 'unknown' and current_element_suffix[1:] not in data['unknown']:
                files_collection['unknown']['files'].append(element)
            
    return files_collection
            
def create_folders_and_move_files(D):
    archives = []
    for key, value in D.items():
        if value['files'] != []:
            try:
                os.mkdir(key)
            except FileExistsError as e:
                pass
            for file in value['files']:
                shutil.move(file, key)
                if key == 'archives':
                    archives.append(file)
    
    return archives

def remove_all_folders(folders_list):
    """Remove all folders"""
    try:
        for folder in folders_list:
            shutil.rmtree(folder)
    except FileNotFoundError:
        pass


def unpack_archives():
    archives = 'archives'
    for archive in Path(archives).iterdir():
        if archive.suffix[1:] in ['zip', 'tar', 'gz', 'tar.gz']:
            folder_archive_name = archive.stem
            path_archive = archives + '/' + folder_archive_name
            
            try:
                os.mkdir(path_archive)
            except FileExistsError:
                pass
            
            shutil.unpack_archive(archive, path_archive + '/')
            os.remove(archive)

def main():
    if len(argv) > 1:
        argument = Path(argv[1])
        folders, files = recursive_analyze(argument)
        files = rename_same_filename(files)
        data = make_structure(files, EXTENS)
        
        create_folders_and_move_files(data)
        remove_all_folders(folders)

        if os.path.isdir('archives'):
            unpack_archives()

        print('Successfully sorted!')

if __name__ == '__main__':
    main()