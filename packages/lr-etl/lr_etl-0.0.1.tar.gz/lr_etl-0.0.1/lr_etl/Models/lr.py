from lr.Config import *
from lr.Models.db.db_handler import Database, DBConfig
from typing import List
from pandas import DataFrame
from lr.use_cases import *
from lr.Libs.file import FileUteis
from lr.Libs.log import LogWrapping, Log
from lr.Models.adapter import DataAdapter
from alive_progress import alive_bar
from lr.Config import *


class LR:

    """
    Handler to process extract, transform and data load.

    LR -> v1
    LA -> v2
    """

    @LogWrapping()
    def handle(config):
        """
         :Basic flow
        -----------
        1. download csv files from a external link which will provided.
        2. read and transform all data source files to dataframes.
        3. create the database connection.
        4. for each dataframe: 
            4.1 adapter the attributes to works with any process type (LR or LA)
            4.2 load the dataframe to database.
        5. clear storage folder.

        Parameters
        ----------
        config: GeneralConfig
            all settings necessary to process works.

        """

        ### Set configs on log handler
        Log.BASE_API = config.apiBaseUrl
        Log.Cliente = config.clienteName

        ### extract data
        # extractor = ExtractDataSource(config.linkDownload)
        # extractor.extract()

        ### parse data: convert and format into dataframes
        parser = ParseData()
        datasets: List[DataFrame] = parser.parse()

        ### create the database connection
        db = Database(config.dbConfig)
        conn = db.connect()

        ### repository handler which will realize databse operations
        repository = Repository(conn, config.tablename)

        with alive_bar(len(datasets)) as bar:
            for df in datasets:
                info = DataAdapter(conn, df, config.dataVersion)
                repository.load(df, info)

                # if config.dataVersion == "v2":
                #     repository.updateManagementTables()
                #     ExecuteRebuild.handle(config.weekday)

                bar()

        FileUteis.clearFolder(STORAGE_FOLDER)
            