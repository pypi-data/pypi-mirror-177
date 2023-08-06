from typing import List
from pandas import DataFrame
from os import listdir
import os
import pandas as pd
from lr_etl.Config import *


class ParseData:

    def __init__(self, dataVersion="v2") -> None:
        self.dataVersion = dataVersion
    
    def parse(self) -> List[DataFrame]:
        """Converte os arquivos csv das listas em uma lista de dataframes"""
        listasStorage = listdir(STORAGE_FOLDER)
        listasStorage = [item for item in listasStorage if '.csv' in item and item not in ['tbl_periodicidade.csv', 'tbl_sublista.csv', 'lista_atencao.csv', 'tbl_fontes.csv']]
        listas = [pd.read_csv(os.path.join(STORAGE_FOLDER, item), encoding="utf8") for item in listasStorage]
        for i, df in enumerate(listas):
            if 'Unnamed: 0' in df.columns:
                listas[i] = df.drop(columns=df.columns[0])
        return listas