import os 
from lr_etl.Libs.file import FileUteis

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

BASE_PATH = os.getcwd()
ENV = "PRD"

STORAGE_FOLDER = FileUteis.createFolder(os.path.join(BASE_PATH, "storage"))
BCP_LOG_PATH = os.path.join(BASE_PATH, "imports")
IMPORT_BAT = os.path.join(BASE_PATH, "import.bat")

TABLEIDCOL = {"ST_LISTA_RESTRITIVA_FIRA": "ID_LISTA", "ListaAtencao": "IdSublista"}


