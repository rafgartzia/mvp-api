from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Progressao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Progressões", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
progressao_tag = Tag(name="PrProgressão", description="Adição, visualização e remoção de progressões à base")
#comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um progressoes cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/progressao', tags=[progressao_tag],
          responses={"200": ProgressaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_progressao(form: ProgressaoSchema):
    """Adiciona uma nova Progressão à base de dados

    Retorna uma representação das progressões.
    """
    progressão = Progressao(
        cod_mapa=form.cod_mapa,
        texto=form.texto,
        ramo=form.ramo,
        etapa=form.etapa
        )
    logger.debug(f"Adicionando nova progressão: '{progressao.cod_mapa}' - '{progressao.texto}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando progressao
        session.add(progressao)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada progressão: '{progressao.cod_mapa}' - '{progressao.texto}'")
        return apresenta_produto(progressao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Progressão já salva na base :/"
        logger.warning(f"Erro ao adicionar progressao '{progressao.cod_mapa}' - '{progressao.texto}'', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar  progressão: '{progressao.cod_mapa}' - '{progressao.texto}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/progressao', tags=[produto_tag],
         responses={"200": ListagemProgressoesSchema, "404": ErrorSchema})
def get_progressao():
    """Faz a busca por todos os Progressao cadastrados

    Retorna uma representação da listagem de progressoes.
    """
    logger.debug(f"Coletando progressoes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    progressoes = session.query(Progressao).all()

    if not progressoes:
        # se não há progressoes cadastrados
        return {"progressoes": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(progressoes))
        # retorna a representação de progressao
        print(progressoes)
        return apresenta_progressoes(progressoes), 200


@app.get('/progressao', tags=[produto_tag],
         responses={"200": ProgressaoViewSchema, "404": ErrorSchema})
def get_produto(query: ProgressaoBuscaSchema):
    """Faz a busca por um Progressao a partir do id do progressao

    Retorna uma representação dos progressoes e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre progressao #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    progressao = session.query(Progressao).filter(Progressao.id == produto_id).first()

    if not progressao:
        # se o progressao não foi encontrado
        error_msg = "Progressao não encontrado na base :/"
        logger.warning(f"Erro ao buscar progressao '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Progressao econtrado: '{progressao.nome}'")
        # retorna a representação de progressao
        return apresenta_produto(progressao), 200


@app.delete('/progressao', tags=[produto_tag],
            responses={"200": ProgressaoDelSchema, "404": ErrorSchema})
def del_produto(query: ProgressaoBuscaSchema):
    """Deleta um Progressao a partir do nome de progressao informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre progressao #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Progressao).filter(Progressao.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado progressao #{produto_nome}")
        return {"mesage": "Progressao removido", "id": produto_nome}
    else:
        # se o progressao não foi encontrado
        error_msg = "Progressao não encontrado na base :/"
        logger.warning(f"Erro ao deletar progressao #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProgressaoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um progressoes cadastrado na base identificado pelo id

    Retorna uma representação dos progressoes e comentários associados.
    """
    produto_id  = form.produto_id
    logger.debug(f"Adicionando comentários ao progressao #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo progressao
    progressao = session.query(Progressao).filter(Progressao.id == produto_id).first()

    if not progressao:
        # se progressao não encontrado
        error_msg = "Progressao não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao progressao '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao progressao
    progressao.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao progressao #{produto_id}")

    # retorna a representação de progressao
    return apresenta_produto(progressao), 200
