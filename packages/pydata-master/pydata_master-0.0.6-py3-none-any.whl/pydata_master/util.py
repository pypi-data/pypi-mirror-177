# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import yaml
import os
import requests
import shutil
from trafilatura import fetch_url, extract
import subprocess

# Working with file systems
def lmt_detect():
    """Detect the running OS and return file path delimiter"""
    if os.name == 'nt':
        lmt = '\\'
    else:
        lmt = '/'
    return lmt

ROOT_DIR = os.path.abspath(os.curdir)

def file_ls(directory=ROOT_DIR):
    """List all file in the root directory"""
    data = []
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            data.append(entry)
    return data

def subdir_ls(basepath=ROOT_DIR):
    """List all subdirectories in the root folder"""
    data = []
    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)):
            data.append(entry)
    return data

# Data loading
def read_txt(path_to_file):
    """Read a plain text file"""
    with open(path_to_file) as f:
        content = f.read()
    return content

# Config file loading
def yaml_cred(item_name, cred_path):
    """Read YAML config file"""
    with open(cred_path) as file: 
        documents = yaml.full_load(file)
        for item, doc in documents.items():
            if item == item_name:
              secret_key = doc
              return secret_key

# Download remote resource
def get_google_font(font_family):
    """Download & extract a Google font to local folder"""
    lmt = lmt_detect()
    font_url = 'https://fonts.google.com/download?family={}'.format(font_family)
    response = requests.get(font_url)
    file_name = ROOT_DIR + lmt + '{}.zip'.format(font_family)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file_name, lmt.join([ROOT_DIR, 'font', font_family]))

def web_to_text(url):
    """Convert a web page content to text file"""
    downloaded = fetch_url(url)
    result = extract(downloaded)
    return result

# Run cmd command
def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass
