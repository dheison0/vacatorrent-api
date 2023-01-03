# VacaTorrent API

Uma API criada usando extração de dados do website [VacaTorrent](http://vacatorrent.com)
com a biblioteca BeautifulSoup versão 4 e o servidor assíncrono feito usando o framework
Sanic para obter uma melhor velocidade

## Desenvolvimento: v2

Regras:

  - Usar camel case no lugar de snake case;
  - Criar classes em cada extrator;
  - O código deve ser flexivél;
  - Usar poucos parâmetros em cada função;
  - Evitar o uso de multiplos blocos embutidos;
  - Todo retorno da API deve ser padronizado.
  - Deve ser feita no formato REST Full;


A fazer:

  - [ ] Rota de página inicial:
    - [X] Extrair: Título, Gênero, Capa, Ano, Classificação IMDB, URL direta e path;
    - [ ] Suportar navegação entre páginas.

  - [ ] Página de download:
    - [X] Extrair: Título, Sinopse, Classificação IMDB, Capa e Links magneticos;
    - [ ] Recolher lista de recomendados.

  - [ ] Página de pesquisa:
    - [X] Extrair: Título, Sinopse, Capa e path;
    - [ ] Suportar navegação limitada.
