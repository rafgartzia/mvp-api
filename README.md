# Pós Eng. Soft. PUC-Rio
## MVP Dev. Full Stack Básico

### Intro
Nessa proposta de MVP pretendemos criar uma solução para acompanhamento das progressões dos jovens no Movimento Escoteiro.

As progressões são atividade/tarefas que devem ser realizadas pelos jovens a fim de desenvolverem as seguintes competências: física, intelectual, social, espiritual, caráter e afetiva.

Embora exita um aplicativo para Android que permite o acompanhamento das progressões de cada jovem, não há funconalidade para a apresentação gráfica e consolidade das progressões de um grupo de jovens.

Essa apresentação facilitaria o diagnóstico de competências do jovens e auxiliaria na proposiçao de atividades para os jovens.

Nesse MVP apresentamos a implentação da parte realtiva às Progressões.

### Modelo do Banco de Dados

Os modelos estão disponíveis nos seguintes links:

[Conceitual](https://app.brmodeloweb.com/#!/publicview/6756350fec67b41b61bd77e6)

[Lógico](https://app.brmodeloweb.com/#!/publicview/67563463ec67b41b61bd77c7)

Nesse MVP inciamos com a tabela Progressao.

### Execução da API

É recomendado o uso de ambiente virtual. O comando abaixo cria o ambiente de nome ".env".

```
pasta_raiz\python -m venv .env
```
Ativar o ab=mbiente virtual.

Para execução da API será necessária a instalação das bibliotecas listadas no `requirements.txt`.

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
pasta_raiz\pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
