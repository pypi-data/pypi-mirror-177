import pandas as pd


class DataAdapter:
    ids: int
    name: str

    def __init__(self, conn, df, dataVersion) -> None:
        if dataVersion == "v2":
            self.ids = df["IdSublista"].iloc[0]
            sub = pd.read_sql("ListaAtencaoSublista", conn.engine)
            subf = sub[sub["Id"] == self.ids]
            self.name = subf["Nome"].iloc[0]
        else:
            self.ids = df["ID_LISTA"].iloc[0]
            self.name = df["LISTA"].iloc[0]


