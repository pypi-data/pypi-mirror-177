import requests
import zipfile
from lr_etl.Config import *
import io


class ExtractDataSource:

    def __init__(self, link) -> None:
        self.link = link

    def extract(self) -> None:
        """Realiza o download do arquivo zip contendo as listas no formato CSV do servidor FTP da Fira"""
        r = requests.get(self.link, headers=HEADER, verify=False)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(STORAGE_FOLDER)
