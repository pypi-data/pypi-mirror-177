from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class LogModel:
    NomeProcesso: str
    Cliente: str
    Ambiente: str
    VM: str
    Perfil: str
    DataExecucao: datetime
    Funcao: str
    Duracao: str
    Status: str
    MessageError: str
    ConsumoCPU: str
    ConsumoMemoria: str
    Diretorio: str
    Detalhes: str