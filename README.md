Projeto: concecionária

Tema escolhido

Este projeto implementa um sistema de catálogo e pedidos de carros seguindo a proposta de Concecionária. A ideia é usar diferentes bancos de dados de acordo com o tipo de informação e com a forma como ela é utilizada pela aplicação.

No sistema, o usuário pode:





realizar cadastro, login e troca de senha;



visualizar o catálogo de carros;



adicionar e remover carros do catálogo;



fazer pedidos;



listar pedidos;



cancelar pedidos;



atualizar o status de um pedido.

Arquitetura do projeto

O projeto segue o modelo pedido no enunciado, com frontend se comunicando com o backend, e o backend se comunicando com três bancos distintos: um relacional e dois não relacionais.

graph LR
    FE <--> BE
    BE <--> DuckDB
    BE <--> MongoDB
    BE <--> Redis






FE: páginas HTML servidas pelo backend para interação do usuário.



BE: aplicação em Python com FastAPI, responsável por receber as requisições e acessar os bancos.



DuckDB: banco relacional usado para armazenar clientes/usuários.



MongoDB: banco orientado a documentos usado para armazenar o catálogo de carros.



Redis: banco chave-valor usado para armazenar pedidos.

Justificativa dos bancos usados

1. DuckDB (Relacional)

O DuckDB foi utilizado para armazenar os dados de usuários/clientes, com campos como nome e senha. Esse tipo de dado possui estrutura bem definida e combina com o modelo relacional.

Ele foi escolhido porque:





os dados de usuários são estruturados;



operações como busca, validação e atualização de senha são naturalmente relacionais;



o backend faz consultas SQL diretamente sobre a tabela client.

2. MongoDB (Document Storage)

O MongoDB foi usado para armazenar os carros do catálogo. Como cada carro é tratado como um documento, esse modelo facilita inserir, listar e remover itens sem exigir um esquema rígido.

Ele foi escolhido porque:





o catálogo pode ser representado naturalmente como documentos;



a aplicação já manipula os carros como dict;



operações de inserção, listagem e remoção ficam simples.

3. Redis (NoSQL chave-valor)

O Redis foi usado para os pedidos. Cada pedido é salvo com uma chave no formato pedido:id, contendo informações como carro, quantidade, cidade e status.

Ele foi escolhido porque:





pedidos podem ser acessados rapidamente por identificador;



o modelo chave-valor atende bem ao fluxo de criação, consulta, atualização e remoção;



o status do pedido pode ser alterado com facilidade.

Implementação do backend

O backend foi implementado em Python usando FastAPI.

Ele centraliza o acesso aos três bancos e expõe rotas HTTP para as operações da aplicação. Entre as principais rotas implementadas estão:

Usuários





POST /login



POST /cadastro



POST /mudarsenha

Catálogo





GET /catalogo



GET /dados



POST /adicionar



POST /deletar

Pedidos





GET /pedido



GET /pedidos



POST /fazer_pedido



POST /cancelar_pedido



POST /atualizar_pedido

Assim, o backend atende ao requisito de realizar operações de CRUD ao longo dos serviços da aplicação, conforme solicitado no enunciado.

Como executar o projeto

Pré-requisitos

Antes de executar, é necessário ter instalado:





Python 3.10 ou superior;



pip;



acesso à internet para conexão com MongoDB e Redis;



os arquivos frontend na mesma pasta do main.py, como index.html, catalogo.html e pedido.html.

Instalação das dependências

Instale as bibliotecas Python usadas no projeto:

pip install fastapi uvicorn duckdb pymongo redis pydantic


Configuração necessária

O backend utiliza:





um arquivo DuckDB local;



uma conexão com MongoDB Atlas;



uma instância Redis remota.

Importante:





o caminho do DuckDB está fixado no código e pode precisar ser ajustado para a sua máquina;



as credenciais de MongoDB e Redis estão definidas diretamente no arquivo main.py.

Execução

Para iniciar o servidor:

python main.py


O sistema será executado localmente em:

http://127.0.0.1:8000


Serviços utilizados

Os serviços/bancos utilizados no projeto são:





DuckDB para usuários;



MongoDB para catálogo de carros;



Redis para pedidos;



FastAPI/Uvicorn para o backend web.

Recursos necessários no repositório

Para atender ao enunciado, o repositório deve conter:





todo o código-fonte do projeto;



este README.md;



os arquivos de frontend;



qualquer recurso necessário para executar o sistema em um ambiente novo.



 
