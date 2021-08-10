import requests
from bs4 import BeautifulSoup
from pathlib import Path
import zipfile

#for Windows only
resp = requests.get('https://github.com/mozilla/geckodriver/releases')
soup = BeautifulSoup(resp.content, features='html.parser')
version = soup.find(class_="repository-content").find(class_='release-header').find('a').text
url = f'https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-win64.zip'

save_dir = Path('FirefoxDrivers/Windows')
zip_file = save_dir.joinpath(f'geckodriver-v{version}-win64.zip')
file_resp = requests.get(url, allow_redirects=True)
zip_file.write_bytes(file_resp.content)
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(save_dir)
zip_file.unlink()