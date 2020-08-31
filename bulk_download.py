#!/usr/bin/env python3

import requests
import re
import tqdm
import os

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0][1:-1]

URL_length = 66
DOWNLOAD_PATH = 'downloaded'

if __name__ == '__main__':

    file_count = 0
    download_URLs = []
    with open('res/20200827_Audio Library - YouTube.html', 'r') as f:
        for line in f:
            idx = line.find('https://www.youtube.com/audiolibrary_download?vid=')
            if idx >= 0:
                download_URL = line[idx:idx+URL_length]
                download_URLs.append(download_URL)
                print(download_URL)
                file_count += 1

    print(file_count)

    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    for download_URL in tqdm.tqdm(download_URLs):
        r = requests.get(download_URL)
        filename = get_filename_from_cd(r.headers.get('content-disposition'))
        with open(os.path.join(DOWNLOAD_PATH, filename), 'wb') as f:
            f.write(r.content)
