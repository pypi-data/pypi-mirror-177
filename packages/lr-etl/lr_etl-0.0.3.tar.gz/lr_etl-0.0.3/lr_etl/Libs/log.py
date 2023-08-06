import logging
from dataclasses import asdict
from lr_etl.Models.entities.log_model import LogModel
from lr_etl.Config import *
from functools import wraps
from lr_etl.Libs.date import DateUteis
import requests
import json, os
from timeit import default_timer as timer
from datetime import timedelta
import psutil


class Log:

    Cliente: str = None
    BASE_API: str = None
  
    log_format = 'Data/Hora: %(asctime)s | level: %(levelname)s | mensagem: %(message)s'
    logging.basicConfig(filename='log_atualizacao_listas.log', level=logging.INFO, format=log_format)
    logger = logging.getLogger('root')

    global_exceptions = []
    has_exceptions: bool = False

    def setBaseUrl(cls, url: str):
        cls.BASE_API = url

    def setClienteName(cls, name):
        cls.Cliente = name

    @classmethod
    def info(cls, message):
        cls.logger.info(message)
        cls.global_exceptions.append(message)
        
    @classmethod
    def warning(cls, message):
        cls.logger.warning(message)
        cls.global_exceptions.append(message)
        cls.has_exceptions = True

    @classmethod
    def post_log(cls, model: LogModel):
        try:
            cls.info("enviando log...")
            d = asdict(model)
            response = requests.post(cls.BASE_API + "log-robos", headers={"Content-Type": "application/json"}, data=json.dumps(d))
            if response.status_code == 200:
                cls.info("log enviado...")
            else:
                cls.info("falha ao enviar o log, message: {}".format(response.content))
        except Exception as err:
            cls.warning("erro ao enviar log: {}".format(str(err)))

def LogWrapping(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        def wrapped(*farg, **fkw):
            try:
                start = timer()

                retorno = None
                trace = None

                main = func.__name__
                Log.info("{} started".format(main))
                retorno = func(*farg)
                Log.info("{} finished".format(main))

                status = "SUCESSO"
               
            except Exception as err:
                Log.warning(str(err))
                status = "FALHA"
                trace = str(err)
            finally:
                log = LogModel(
                    NomeProcesso="LR",
                    Cliente=Log.Cliente,
                    Ambiente=ENV,  
                    Funcao=func.__name__,
                    Status=status,
                    MessageError=trace,
                    DataExecucao=DateUteis.now(fmt="%Y-%m-%d %H:%M"),
                    VM=os.getenv('COMPUTERNAME'),
                    Perfil=os.getlogin(),
                    Duracao=str(timedelta(seconds=timer()-start))[:-3],
                    ConsumoCPU=psutil.cpu_percent(4),
                    ConsumoMemoria=psutil.virtual_memory()[2],
                    Diretorio=os.getcwd(),
                    Detalhes=retorno if main == "insert" and status == "SUCESSO" else None
                )
                Log.post_log(log)
            return retorno
               
        return wrapped
    return wrapper




