import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install('pandas')
install('bs4')

import time
import requests
import pandas as pd
import zipfile
from bs4 import BeautifulSoup

url = 'https://glossaries.dila.edu.tw/data/mahavyutpatti.dila.tei.p5.xml.zip'

year = str(time.gmtime().tm_year)
month = str(time.gmtime().tm_mon)
day = str(time.gmtime().tm_mday)

date = day + '/' + month '/' + year

def download_url(url=url, data='data/Mahavyutpatti_' + date + '.zip', chunk_size=128):
    r = requests.get(url, stream=True)
    with open(data/, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

with ZipFile('data/Mahavyutpatti_' + date + '.zip') as zip:
    zip.extractall()
    
with open('data/Mahavyutpatti_' + date + '.xml', 'r') as f:
    data = f.read()
bs_data = BeautifulSoup(data, "xml")
data = bs_data.find_all('entry')

out = {}
for i in range(len(data)):

    skt_str = data[i].find('orth', {'xml:lang':'san-Latn'}).text
    tib_str = data[i].find('cit', {'xml:lang':'bod-Tibt'}).text.strip()

    out[tib_str] = skt_str

out = pd.DataFrame.from_dict(out, 'index').reset_index()
out.columns = ['Tibetan-Word', 'Sanskrit-Word']

out['Tibetan-Word'] = out['Tibetan-Word'].str.strip()
out['Sanskrit-Word'] = out['Sanskrit-Word'].str.strip()

out.to_csv('data/Mahavyutpatti')
