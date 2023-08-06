
from lr.Libs.log import Log, LogWrapping
from lr.Models.adapter import DataAdapter
from lr.Config import *
import numpy
from pandas import DataFrame


class Repository:

    def __init__(self, conn, tablename) -> None:
        self.tablename = tablename
        self.conn = conn

    @LogWrapping()
    def delete(self, ids):
        query = "DELETE FROM " + self.tablename + \
                "WHERE" + TABLEIDCOL[self.tablename] + " = " + str(ids)

        self.conn.session.execute(query)
        self.conn.session.commit()

    @LogWrapping()
    def insert(self, df: DataFrame, info: DataAdapter):
        df.to_sql(
            name=self.tablename,
            con=self.conn.engine,
            if_exists='replace',
            index=False,
            method="multi",
            chunksize=100
        )
        return "id: {} name: {}".format(info.ids, info.name)

    def load(self, df: DataFrame, info: DataAdapter):
        # self.delete(info.ids)

        if df.shape[0] > 200000:
            groups = numpy.array_split(df, 50)
            for group in groups: 
                self.insert(group, info)
        else:
            self.insert(df, info)

        
