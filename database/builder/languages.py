import csv
from io import StringIO

import requests

ISO_639_3_DOWNLOAD = 'https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Name_Index.tab'
ISO_639_2_DOWNLOAD = 'https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt'

ISO_639_3 = {}
ISO_639_2 = {}


def get_iso639_2():
    r = requests.get(ISO_639_2_DOWNLOAD)
    r.encoding = "UTF-8-SIG"
    if r.status_code == 200:
        with StringIO(r.text) as file:
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                ISO_639_2[row[0]] = row[3]
            del reader
        # this is ISO 639-5
        ISO_639_2['gmw'] = 'West Germanic'
    del r


def get_iso639_3():
    r = requests.get(ISO_639_3_DOWNLOAD)
    r.encoding = "UTF-8-SIG"
    if r.status_code == 200:
        with StringIO(r.text) as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                ISO_639_3[row['Id']] = row['Print_Name']
            del reader
        # Not actually from this ISO, or out of date data, but sill can be put in the database
        ISO_639_3['nah'] = 'Nahuatl'
        ISO_639_3['wit'] = 'Wintu'
        ISO_639_3['kzj'] = 'Coastal Kadazan'
    del r


def get_language_name(iso_code: str):
    if iso_code.startswith("p_"):
        if len(ISO_639_2) == 0:
            get_iso639_2()
        return 'Proto {0}'.format(ISO_639_2[iso_code[2::]])
    else:
        if len(ISO_639_3) == 0:
            get_iso639_3()
        return ISO_639_3[iso_code]
