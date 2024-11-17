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
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
progressao_tag = Tag(name="Progressão", description="Adição, visualização e remoção de progressão à base")



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
        logger.warning(f"Erro ao adicionar progressão '{progressao.texto}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar progressão '{progressao.texto}', {error_msg}")
        return {"mesage": error_msg}, 400
@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


