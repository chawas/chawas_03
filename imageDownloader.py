from sys import dont_write_bytecode

import requests

def download_files(url):
    local_filename = url.split('/home/chawas/Development/python/selenium/projects/chawas_03/')[-1]
    print(local_filename)

download_files("https://charts.ecmwf.int/products/opencharts_meteogram?base_time=202409230000&epsgram=classical_10d&lat=-18.1833&lon=31.55&station_name=Marondera")