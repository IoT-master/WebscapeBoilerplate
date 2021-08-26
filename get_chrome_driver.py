import zipfile
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

CHROME_VERSION = 92
current_platform = os.name

dir_platform = {
    'posix': './ChromeDrivers/Linux',
    'darwin': './ChromeDrivers/Mac',
    'nt': './ChromeDrivers/Windows'
}
save_dir = Path(dir_platform[current_platform])

chromedriver_platform = {
    'posix': 'chromedriver',
    'darwin': 'chromedriver',
    'nt': 'chromedriver.exe'
}
chromedriver = save_dir.joinpath(chromedriver_platform[current_platform])

if not chromedriver.exists():

    resp = requests.get(
        'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix=')
    soup = BeautifulSoup(resp.text, features="lxml")
    newest_version = None
    for segment in soup.find_all('commonprefixes'):
        if segment.find('prefix').text.split('.')[0] == str(CHROME_VERSION):
            newest_version = segment.find('prefix').text
            break
    if newest_version is None:
        raise ValueError()
    

    url_platform = {
        'posix': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_linux64.zip',
        'darwin': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_mac64.zip',
        'nt': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_win32.zip'
    }
    dir_platform = {
        'posix': './ChromeDrivers/Linux',
        'darwin': './ChromeDrivers/Mac',
        'nt': './ChromeDrivers/Windows'
    }
    url = url_platform[current_platform]
    zip_file = save_dir.joinpath('ChromeDriver.zip')
    file_resp = requests.get(url, allow_redirects=True)
    zip_file.write_bytes(file_resp.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(save_dir)
    zip_file.unlink()
