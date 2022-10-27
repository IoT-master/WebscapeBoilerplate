import requests
from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
import os
import tarfile

current_platform = os.name
dir_platform = {
    "posix": "./FirefoxDrivers/Linux",
    "darwin": "./FirefoxDrivers/Mac",
    "nt": "./FirefoxDrivers/Windows",
}

resp = requests.get("https://github.com/mozilla/geckodriver/releases")
soup = BeautifulSoup(resp.content, features="html.parser")
version = (
    soup.find(id="repo-content-pjax-container").find(class_="Link--primary").text
)

if current_platform == "nt":

    url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-win64.zip"

    save_dir = Path("FirefoxDrivers/Windows")
    zip_file = save_dir.joinpath(f"geckodriver-v{version}-win64.zip")
    file_resp = requests.get(url, allow_redirects=True)
    zip_file.write_bytes(file_resp.content)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(save_dir)
    zip_file.unlink()
else:

    url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-linux64.tar.gz"

    save_dir = Path("FirefoxDrivers/Linux")
    zip_file = save_dir.joinpath(f"geckodriver-v{version}-linux64.tar.gz")
    file_resp = requests.get(url, allow_redirects=True)
    zip_file.write_bytes(file_resp.content)
    with tarfile.open(zip_file) as tar_ref:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar_ref, save_dir)
    zip_file.unlink()
