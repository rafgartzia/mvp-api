from pydantic import BaseModel
from typing import Optional, List
from model.progressao import Progressao



class ProgressaoSchema(BaseModel):
    """ Define como uma nova progressao a ser inserida deve ser representado
    """
    cod_mapa: int = 10
    texto: str = "Texto da progressão"
    ramo: str = "Escoteiro"
    etapa: str = "Pista"


class ProgressaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no codigo do mapa da progressão.
    """
    cod_mapa: int = 10


class ListagemProgressoesSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    progressoes:List[ProgressaoSchema]


def apresenta_progressoes(progressoes: List[ProgressaoSchema]):
    """ Retorna uma representação da progressão seguindo o schema definido em
        ProgressaoViewSchema.
    """
    result = []
    for progressao in progressoes:
        result.append({
            "cod_mapa": progressao.cod_mapa,
            "texto": progressao.texto,
            "ramo": progressao.ramo,
            "etapa": progressao.etapa
        })

    return {"progressoes": result}


class ProgressaoViewSchema(BaseModel):
    """ Define como uma progressão será retornado.
    """
    id: int = 1
    cod_mapa: int = 10
    texto: str = "Texto da progressão"
    ramo: str = "Escoteiro"
    etapa: str = "Pista"



class ProgressaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    cod_mapa: str
    texto: str

def apresenta_progressao(progressao: Progressao):
    """ Retorna uma representação da progressão seguindo o schema definido em
        ProgressaoViewSchema.
    """
    return {
        "cod_mapa": progressao.cod_mapa,
        "texto": progressao.texto,
        "ramo": progressao.ramo,
        "etapa": progressao.etapa
    }
