import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

url = 'http://glossaries.dila.edu.tw/data/mahavyutpatti.dila.tei.p5.xml.zip'
subprocess.run(["wget", "--no-check-certificate", "http://glossaries.dila.edu.tw/data/mahavyutpatti.dila.tei.p5.xml.zip"])

install('pandas')
install('bs4')
install('requests')

import time
import requests
import pandas as pd
import zipfile
from bs4 import BeautifulSoup

#year = str(time.gmtime().tm_year)
#month = str(time.gmtime().tm_mon)
#day = str(time.gmtime().tm_mday)
#date = day + '/' + month + '/' + year

#r = requests.get(url, allow_redirects=True, verify=False)

#open('Mahavyutpatti.zip', 'wb').write(r.content)

with zipfile.ZipFile('mahavyutpatti.dila.tei.p5.xml.zip') as zip:
    zip.extractall()
    
with open('mahavyutpatti.dila.tei.p5.xml', 'r') as f:
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
