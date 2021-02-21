import csv
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile

import requests

DAB_FILE = 'https://cs.rutgers.edu/~gd343/downloads/etymwn-20130208.zip'


def get_etymologies():
    # get the dataset
    r = requests.get(DAB_FILE)
    if r.status_code == 200:
        f = BytesIO(r.content)
        del r
        with ZipFile(f, 'r') as zipfile:
            with TextIOWrapper(zipfile.open('etymwn.tsv', 'r'), 'utf-8-sig') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for line in reader:
                    s_lang, s_word = line[0].split(': ', 1)
                    t_lang, t_word = line[2].split(': ', 1)
                    yield {
                        's_lang': s_lang,
                        's_word': s_word,
                        't_lang': t_lang,
                        't_word': t_word,
                        'relationship': line[1].split(':')[1]
                    }
                del reader
        del f
