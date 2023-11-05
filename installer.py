import requests
from tqdm import tqdm
import os
import string
import random
import zipfile
import shutil
import pathlib
import winshell
import win32com.client

root_path: str = os.path.join(os.getenv('APPDATA'), 'ziqva-installer')
tmp_path: str = os.path.join(root_path, 'tmp')
apps_path: str = os.path.join(root_path, 'apps')

if not os.path.exists(root_path) :
    os.makedirs(root_path)

if not os.path.exists(tmp_path) :
    os.makedirs(tmp_path)

if not os.path.exists(apps_path) :
    os.makedirs(apps_path)

def generate_file_name(ext: str, length: int) -> str:
    fn: str = ''
    for i in range(length) :
        fn += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    return f'{fn}.{ext}'

def download(download_url: str, title: str) -> str:
    target_file_path: str = os.path.join(tmp_path, generate_file_name('zip', 50))
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(target_file_path, 'wb') as file, tqdm(
        desc=title,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar :
        for data in response.iter_content(chunk_size=1024) :
            file.write(data)
            bar.update(len(data))
    return target_file_path

def create_desktop_shortcut(executable_path: str, appname: str) -> bool :
    desktop = winshell.desktop()
    path = os.path.join(desktop, f'{appname}.lnk')
    if os.path.exists(path) and os.path.isfile(path) :
        os.unlink(path)
    wd = os.path.dirname(executable_path)
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(path)
    shortcut.Targetpath = executable_path
    shortcut.WorkingDirectory = wd
    shortcut.IconLocation = executable_path
    shortcut.save()
    return True

def remove_files_in_dir(path: str) :
    shutil.rmtree(path)

def install(filepath: str, appname: str, version: str) -> str or None:
    target_path = os.path.join(apps_path, appname)
    if not os.path.exists(target_path) :
        os.makedirs(target_path)
    else :
        remove_files_in_dir(target_path)
        if not os.path.exists(target_path) :
            os.makedirs(target_path)

    with zipfile.ZipFile(filepath, 'r') as zip_file :
        file_list = zip_file.namelist()
        with tqdm(total=len(file_list), unit=' file', desc='Extracting ') as pbar :
            for file in file_list :
                zip_file.extract(file, target_path)
                pbar.update(1)


    files: list = os.listdir(target_path)
    file_details: list = []
    for file in files :
        if pathlib.Path(file).suffix != '.exe':
            continue
        file_details.append({
            'filename': file,
            'filepath': os.path.join(target_path, file),
            'extension': pathlib.Path(file).suffix
        })

    shutil.rmtree(tmp_path)
    for file_detail in file_details:
        filename = str.lower(file_detail['filename'])
        app_name = str.lower(appname)
        if filename == f'{app_name}.exe' or filename == f'{app_name} {version}.exe' or filename == f'{app_name} - {version}.exe' :
            return file_detail['filepath']

    for fd in file_details:
        if str.lower(appname) in str.lower(fd['filename']) :
            return fd['filepath']

    if len(file_details) < 1:
        return None
    return file_details[0]['filepath']