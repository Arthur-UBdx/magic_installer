import zipfile
import os
import shutil
import time
import requests

APPDATA = os.getenv('APPDATA')
MINECRAFT_FOLDER = os.path.join(APPDATA, '.minecraft')
MODS_FOLDER = os.path.join(APPDATA, '.minecraft', 'mods')
MODS_URL = 'https://github.com/Arthur-UBdx/mods_minecraft/zipball/main'
FABRIC_FOLDER = os.path.join(MINECRAFT_FOLDER, 'fabric_installers')
FABRIC_URL = 'https://github.com/Arthur-UBdx/fabric_minecraft/zipball/main'


def unzip_files(zip_path):
    folder = os.path.dirname(zip_path)
    for k in range(10):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(folder)
        folders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
        if folders: 
            for file in os.listdir(os.path.join(folder, folders[0])):
                os.rename(os.path.join(folder, folders[0], file), os.path.join(folder, file))
            shutil.rmtree(os.path.join(folder, folders[0]))
            os.remove(zip_path)
            return 0
        else:
            continue
    else:
        return 1
    
def install_fabric():
    try:
        shutil.rmtree(FABRIC_FOLDER)
    except FileNotFoundError:
        pass
    if not os.path.isdir(os.path.join(MINECRAFT_FOLDER, 'fabric_installers')):
        os.mkdir(os.path.join(MINECRAFT_FOLDER, 'fabric_installers'))
    
    r = requests.get(FABRIC_URL, allow_redirects=True)
    open(os.path.join(FABRIC_FOLDER, 'fabric.zip'), 'wb').write(r.content)
    while not os.path.isfile(os.path.join(FABRIC_FOLDER, 'fabric.zip')) or os.path.getsize(os.path.join(FABRIC_FOLDER, 'fabric.zip')) == 0:
        time.sleep(1)
    if unzip_files(os.path.join(FABRIC_FOLDER, 'fabric.zip')):
        raise Exception("Un zipping error")
        return -1
    for file in os.listdir(FABRIC_FOLDER):
        print(f'Found file: {file}')
        if file.endswith('.exe'):
            print('Starting exe')
            os.system(f'cd {FABRIC_FOLDER} && {file}')
            return 0
    else:
        raise FileNotFoundError('No .exe file found in fabric_installers folder.')
        return -1

def install_mods():
    if not os.path.isdir(MODS_FOLDER):
        os.mkdir(MODS_FOLDER)
    
    r = requests.get(MODS_URL, allow_redirects=True)
    open(os.path.join(MODS_FOLDER, 'mods.zip'), 'wb').write(r.content)
    while not os.path.isfile(os.path.join(MODS_FOLDER, 'mods.zip')) or os.path.getsize(os.path.join(MODS_FOLDER, 'mods.zip')) == 0:
        time.sleep(1)
    if not unzip_files(os.path.join(MODS_FOLDER, 'mods.zip')):
        return -1
    return 0

def remove_all_mods():
    shutil.rmtree(MODS_FOLDER)
    os.mkdir(MODS_FOLDER)
    return 0

if __name__ == '__main__':
    install_fabric()

    print('This script is not meant to be run directly.')
    exit(1)