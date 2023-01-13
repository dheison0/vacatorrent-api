# VacaTorrent API

Uma API criada usando extração de dados do website [VacaTorrent] com a
biblioteca BeautifulSoup versão 4 e o servidor assíncrono feito usando o
framework Sanic para obter uma melhor velocidade.


## Colocando a API online

Para iniciar a API em um servidor você precisa do docker e clonar esse
repositório, dentro da pasta dele rode o comando:

```bash
docker build -t vacatorrent .
```

E espere a criação da imagem, logo após isso inicie o container como daemon e
exporte a porta 5000 para fora do container, com isso você vai ter acesso a
API fora do containner.

Exemplo:

```bash
docker run -d \
  --name vacatorrent \
  -p 1337:5000 \
  vacatorrent:latest
```


## Documentação

A API possui uma página de documentação localizada em `/docs/redoc` e
`/docs/swagger` com a descrição de cada chamada possivel de ser feita e seus
valores de retorno conforme cada código de status.


[VacaTorrent]: <http://vacatorrent.com>
