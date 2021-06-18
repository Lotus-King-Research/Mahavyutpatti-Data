import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install(pandas)
install(zipfile)
install(BeautifulSoup)

import pandas as pd
import zipfile
from bs4 import BeautifulSoup

url = '''https://glossaries.dila.edu.tw/data/mahavyutpatti.dila.tei.p5.xml.zip'''

with zipfile.ZipFile(url, 'r') as zip_ref:
    zip_ref.extractall(data)

with open('data/mahavyutpatti.dila.tei.p5.xml', 'r') as f:
    data = f.read()
print("1")
bs_data = BeautifulSoup(data, "xml")
print("2")
data = bs_data.find_all('entry')

out = {}
print("3")
for i in range(len(data)):

    skt_str = data[i].find('orth', {'xml:lang':'san-Latn'}).text
    tib_str = data[i].find('cit', {'xml:lang':'bod-Tibt'}).text.strip()

    out[tib_str] = skt_str

out = pd.DataFrame.from_dict(out, 'index').reset_index()
out.columns = ['Tibetan-Word', 'Sanskrit-Word']

out['Tibetan-Word'] = out['Tibetan-Word'].str.strip()
out['Sanskrit-Word'] = out['Sanskrit-Word'].str.strip()

out.to_csv('data/Mahavyutpatti')
