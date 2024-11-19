from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Progressao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API progressoes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
progressao_tag = Tag(
    name="Progressão", description="Adição, visualização e remoção de progressão à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/progressao', tags=[progressao_tag],
          responses={"200": ProgressaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_progressao(form: ProgressaoSchema):
    """Adiciona uma nova progressão à base de dados

    Retorna uma representação das progressões
    """
    progressao = Progressao(
        cod_mapa=form.cod_mapa,
        texto=form.texto,
        ramo=form.ramo,
        etapa=form.etapa
    )
    logger.debug(f"Adicionando progressão: '{progressao.texto}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(progressao)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada progressão: '{progressao.texto}'")
        return apresenta_progressao(progressao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Progressão já existente na base :/"
        logger.warning(f"Erro ao adicionar progressão '{
                       progressao.texto}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar progressão '{
                       progressao.texto}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/progressoes', tags=[progressao_tag],
         responses={"200": ListagemProgressoesSchema, "404": ErrorSchema})
def get_progressoes():
    """
        Retorna a lista com todas as progressões cadastradas no BD.
    """
    logger.debug(f"Coletando progressões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    progressoes = session.query(Progressao).all()

    if not progressoes:
        # se não há produtos cadastrados
        return {"progressoes": []}, 200
    else:
        logger.debug(f"%d Progressões encontradas" % len(progressoes))
        # retorna a representação de produto
        print(progressoes)
        return apresenta_progressoes(progressoes), 200


@app.get('/progressao', tags=[progressao_tag],
         responses={"200": ProgressaoViewSchema, "404": ErrorSchema})
def get_progressao(query: ProgressaoBuscaSchema):
    """Faz a busca por uma progressão.

    Retorna uma representação dos produtos e comentários associados.
    """
    progressao_cod_mapa = query.cod_mapa
    logger.debug(f"Coletando dados sobre a progressão #{progressao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    progressao = session.query(Progressao).filter(
        Progressao.cod_mapa == progressao_cod_mapa).first()

    if not progressao:
        # se a progressão não foi encontrada
        error_msg = "Progressao não encontrado na base :/"
        logger.warning(f"Erro ao buscar progressão '{
                       progressao_cod_mapa}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Progressão encontrada: '{progressao.nome}'")
        # retorna a representação da progressão
        return apresenta_progressao(progressao), 200


@app.delete('/progressao', tags=[progressao_tag],
            responses={"200": ProgressaoDelSchema, "404": ErrorSchema})
def del_progressao(query: ProgressaoBuscaSchema):
    """Deleta uma Progressao a partir da id da progressão informada

    Retorna uma mensagem de confirmação da remoção.
    """
    progressao_id = unquote(unquote(query.id))
    print(progressao_id)
    logger.debug(f"Deletando dados sobre progressao #{progressao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Progressao).filter(
        Progressao.id == progressao_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado progressão #{progressao_id}")
        return {"message": "Progressão removida", "id": progressao_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Progressão não encontrada na base :/"
        logger.warning(f"Erro ao deletar progressão #'{
                       progressao_id}', {error_msg}")
        return {"mesage": error_msg}, 404
