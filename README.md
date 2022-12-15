# VacaTorrent API

Uma API criada usando extração de dados do website [VacaTorrent](http://vacatorrent.com)
com a biblioteca BeautifulSoup versão 4 e o servidor assíncrono feito usando o framework
Sanic para obter uma melhor velocidade

## Uso

As seguintes rotas para obtenção de dados estão disponiveis na versão 1(todas usam o método GET):

> Os tipos de retorno citados aqui podem ser encontrados no arquivo [api/v1/types.py](https://github.com/dheisom/vacatorrent-api/blob/main/api/v1/types.py#L21).

| Rota               | Descrição                                                | Parâmetros                     | Retorno                       |
| :----------------- | :------------------------------------------------------- | :----------------------------- | :---------------------------- |
| /v1/home/{page}    | Obtem a página número {page} de recomendações            | Nenhum                         | Lista de HomeResult           |
| /v1/search         | Procura por algum filme/série/desenho                    | q: Texto, page: Número inteiro | Lista de SearchResult ou erro |
| /v1/download/{key} | Obtem as informações de download de determinado conteúdo | Nenhum                         | Download ou erro              |
