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
    - [ ] Extrair: Título, Gênero, Capa, Ano, Classificação IMDB, URL direta e ID;
    - [ ] Suportar navegação entre páginas.

  - [ ] Página de download:
    - [ ] Extrair: Título, Sinopse, Capa, Links magneticos;
    - [ ] Recolher lista de recomendados.

  - [ ] Página de pesquisa:
    - [ ] Extrair: Título, Sinopse, Capa, ID;
    - [ ] Suportar navegação limitada.
