from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Progressao(Base):
    __tablename__ = 'progressao'

    id = Column("pk_progressao", Integer, primary_key=True)
    # cod_mapa se repetem entre os ramos (Lobinho, Escoteiro e Senior) por isso não está como unique
    cod_mapa = Column(Integer)
    texto = Column(String(350), unique=True, nullable=False)
    ramo = Column(String(20), nullable=False)
    etapa = Column(String(20), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    # comentarios = relationship("Comentario")

    def __init__(self, cod_mapa: int, texto: str, ramo: str,
                 etapa: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Progressão

        Argumentos:
            cod_mapa: código associado a cada progressão na publicação de cada ramo,
            é o mesmo código qe aparece no aplicativo mAPPA.
            texto: descrição da progressão
            ramo: ramo da progressão (lobinho, escoteiro ou sênior)
            etapa: etapa a qual a progressão pertence
        """
        self.cod_mapa = cod_mapa
        self.texto = texto
        self.ramo = ramo
        self.etapa = etapa

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

   # def adiciona_comentario(self, comentario:Comentario):
    #    """ Adiciona um novo comentário ao Produto
     #   """
      #  self.comentarios.append(comentario)
