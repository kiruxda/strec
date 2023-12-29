import os
import requests
from datetime import datetime
import schedule
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = 'y0_AgAAAAAkDuy1AADLWwAAAAD2M2wo3MXhIP-dSECQqyAo45MsixTVf-o'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
def create_folder(path):
    requests.put(f'{URL}?path={path}', headers=headers)
def upload_file(loadfile, savefile, replace=False):
    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)
def backup(savepath, loadpath):
    date_folder = '{0}_{1}'.format(loadpath.split('\\')[-1], datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    create_folder(savepath)
    for address, _, files in os.walk(loadpath):
        create_folder('{0}/{1}/{2}'.format(savepath, date_folder, address.replace(loadpath, "")[1:].replace("\\", "/")))
        for file in files:
            upload_file('{0}\{1}'.format(address, file), '{0}/{1}{2}/{3}'.format(savepath, date_folder, address.replace(loadpath, "").replace("\\", "/"), file))
if __name__ == '__main__':
    schedule.every().day.at("11:00").do(backup('Backup', os.getcwd()))
    while True:
        schedule.run_pending()