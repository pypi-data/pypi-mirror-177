from os import listdir
import os
from typing import List
from pandas import DataFrame
from lr_etl.Libs.log import Log, LogWrapping
from lr_etl.Libs.date import DateUteis
from lr_etl.Models.db import sql_server
from lr_etl.Config import *
import pandas as pd
import requests
import zipfile
import io
import numpy
import os 
from lr_etl.Config import *

def atualizar_gestao_de_listas():
    storage = os.listdir(STORAGE_FOLDER)
    if "tbl_sublista.csv" in storage:
        atualizar_sublista()

def carregar_sublista(conn):
    df = pd.read_sql("ListaAtencaoSublista", conn.engine)
    return df

@LogWrapping()
def download_do_arquivo() -> None:
    """Realiza o download do arquivo zip contendo as listas no formato CSV do servidor FTP da Fira"""
    r = requests.get(DOWNLOAD_LISTA, headers=HEADER, verify=False)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(STORAGE_FOLDER)

@LogWrapping()
def converter_arquivos_para_dataframes() -> List[DataFrame]:
    """Converte os arquivos csv das listas em uma lista de dataframes"""
    listasStorage = listdir(STORAGE_FOLDER)
    listasStorage = [item for item in listasStorage if '.csv' in item and item not in ['tbl_periodicidade.csv', 'tbl_sublista.csv', 'lista_atencao.csv', 'tbl_fontes.csv']]
    listas = [pd.read_csv(os.path.join(STORAGE_FOLDER, item), encoding="utf8") for item in listasStorage]
    for i, df in enumerate(listas):
        if 'Unnamed: 0' in df.columns:
            listas[i] = df.drop(columns=df.columns[0])
    return listas

@LogWrapping()
def atualizar_lista(nome, ids, df) -> None:
    """Realizar o delete e o insert do df atualizado nas listas não diárias."""
    Log.info('Deletando registros existentes...')

    sql_server.session.execute(f'delete from {tblListaAtencao} where IdSublista = {int(ids)}')
    sql_server.session.commit()

    Log.info('Inserindo dados atualizados...')
    if df.shape[0] > 200000:
        groups = numpy.array_split(df, 50)
        for group in groups:
            group.to_sql(tblListaAtencao, sql_server.engine, if_exists='append', index=False, method="multi", chunksize=100)
    else:
        df.to_sql(tblListaAtencao, sql_server.engine, if_exists='append', index=False, method="multi", chunksize=100)

@LogWrapping()
def atualizar_sublista() -> None:
    """Realizar a migração dos dados da tabela ListaAtencaoSublista"""
    df = pd.read_csv(os.path.join(STORAGE_FOLDER, "tbl_sublista.csv"), encoding='utf8')
    sub = pd.read_sql("ListaAtencaoSublista", sql_server.engine)
    
    ids = sub["Id"].tolist()
    for i, row in df.iterrows():
        if int(row["Id"]) in list(map(int, ids)):
            dtatt = row["DataAtualizacaoDados"]
            dtcol = row["DataColetaDados"]
            periodo = row["IdPeriodicidade"]
            fonte = row["IdFonte"]
            id_s = row['Id']

            sql_server.session.execute(f"UPDATE ListaAtencaoSublista SET DataAtualizacaoDados = '{dtatt}' WHERE Id = {id_s}")
            sql_server.session.commit()

            sql_server.session.execute(f"UPDATE ListaAtencaoSublista SET DataColetaDados = '{dtcol}' WHERE Id = {id_s}")
            sql_server.session.commit()

            sql_server.session.execute(f"UPDATE ListaAtencaoSublista SET IdPeriodicidade = {periodo} WHERE Id = {id_s}")
            sql_server.session.commit()

            sql_server.session.execute(f"UPDATE ListaAtencaoSublista SET IdFonte = {fonte} WHERE Id = {id_s}")
            sql_server.session.commit()
        else:
            newdf = df[df["Id"] == int(row[0])]
            del newdf["Id"]
            newdf.to_sql("ListaAtencaoSublista", sql_server.engine, if_exists="append", index=False)

@LogWrapping()
def executar_rebuild():
    sql_server.session.execute("SET NOCOUNT ON; EXEC PR_INDEX :p1", {"p1": tblListaAtencao})
    sql_server.session.commit()