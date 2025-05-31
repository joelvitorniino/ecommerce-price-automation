# Projeto de E-commerce com Flask

Este é um projeto de uma API de e-commerce desenvolvida com Flask, que inclui funcionalidades para gerenciamento de produtos, histórico de preços, automação de preços e cache com Redis. O projeto utiliza SQLite como banco de dados, Flask-CORS para suporte a requisições cross-origin, Flasgger para documentação automática da API com Swagger e Flask-Caching para otimização com Redis. Este README fornece instruções detalhadas para configurar, executar e gerenciar o projeto, incluindo o uso de Docker.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- Python 3.8+
- Docker e Docker Compose
- Git
- pip

## Estrutura do Projeto

```
ecommerce/
├── backend/
│   ├── app/
│   │   ├── commands.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── database/
│   │   ├── tests/
│   │   └── __init__.py
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

- **backend/**: Contém o código da aplicação Flask.
- **run.py**: Ponto de entrada para executar a aplicação Flask.
- **requirements.txt**: Lista de dependências do Python.
- **Dockerfile**: Arquivo de configuração para construir a imagem Docker da aplicação.
- **docker-compose.yml**: Arquivo de configuração para orquestrar a aplicação e o serviço Redis com Docker Compose.

## Instalação

### 1. Clone o Repositório

Clone o repositório para sua máquina local:

```
git clone https://github.com/seu-usuario/ecommerce.git
cd ecommerce
```

### 2. Configuração do Ambiente Local (Sem Docker)

Se preferir rodar a aplicação diretamente no seu sistema, siga estas etapas:

#### a) Crie e ative um ambiente virtual

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### b) Instale as dependências

Certifique-se de que o Redis está instalado e em execução localmente (ou ajuste a configuração para um servidor Redis remoto). Instale as dependências do Python:

```
pip install -r backend/requirements.txt
```

#### c) Configure as variáveis de ambiente

Defina a variável `FLASK_APP` e as configurações do Redis:

```
export FLASK_APP=run.py  # Linux/Mac
set FLASK_APP=run.py     # Windows
export CACHE_REDIS_HOST=localhost  # Linux/Mac
set CACHE_REDIS_HOST=localhost    # Windows
export CACHE_REDIS_PORT=6379      # Linux/Mac
set CACHE_REDIS_PORT=6379         # Windows
export CACHE_REDIS_DB=0           # Linux/Mac
set CACHE_REDIS_DB=0              # Windows
```

> **Nota**: Para rodar localmente, você precisa ter o Redis instalado e em execução. No Windows, você pode usar o WSL ou instalar o Redis manualmente. No Linux/Mac, instale com `sudo apt install redis` ou `brew install redis`.

### 3. Configuração do Banco de Dados

O projeto usa SQLite como banco de dados, que será criado automaticamente no diretório `backend/` com o nome `ecommerce.db`.

#### a) Inicialize o banco de dados

Para criar as tabelas do banco de dados, execute:

```
flask init-db
```

Isso apagará todas as tabelas existentes e criará novas tabelas com base nos modelos definidos.

#### b) Popule o banco de dados com dados de exemplo

Para adicionar produtos de exemplo e histórico de preços, execute:

```
flask seed-db
```

Este comando limpa os dados existentes, adiciona produtos predefinidos e gera um histórico de preços fictício.

### 4. Executando a Aplicação Localmente

Certifique-se de que o Redis está em execução (ex.: `redis-server` no terminal). Para iniciar o servidor Flask em modo de desenvolvimento, execute:

```
flask run
```

A aplicação estará disponível em `http://localhost:5000`. A documentação da API pode ser acessada em `http://localhost:5000/swagger/`.

### 5. Executando com Docker Compose

Para rodar a aplicação com Redis em contêineres Docker, siga estas etapas:

#### a) Certifique-se de que o Docker e o Docker Compose estão instalados

Verifique a instalação com:

```
docker --version
docker-compose --version
```

#### b) Construa e inicie os serviços

No diretório raiz do projeto (onde está o `docker-compose.yml`), execute:

```
docker-compose up --build
```

Isso construirá a imagem Docker da aplicação e iniciará os contêineres para o Flask e o Redis. A aplicação estará disponível em `http://localhost:5000`, e o Redis estará acessível na porta `6379`.

#### c) Inicialize e popule o banco de dados no contêiner

Para inicializar o banco de dados dentro do contêiner, acesse o terminal do contêiner da aplicação:

```
docker-compose exec app bash
```

Dentro do contêiner, execute os seguintes comandos para inicializar e popular o banco de dados:

```
flask init-db
flask seed-db
```

Saia do terminal do contêiner com:

```
exit
```

#### d) Parando o Docker Compose

Para parar os contêineres, pressione `Ctrl+C` no terminal onde o `docker-compose up` está rodando, ou execute:

```
docker-compose down
```

### 6. Acessando a Documentação da API

A API possui documentação automática gerada pelo Flasgger (Swagger). Para acessá-la, abra o navegador e vá para:

```
http://localhost:5000/swagger/
```

Aqui, você pode explorar os endpoints disponíveis, testar requisições e visualizar os modelos de dados.

### 7. Comandos CLI Personalizados

O projeto inclui comandos CLI personalizados para gerenciar o banco de dados:

- `flask init-db`: Apaga e recria todas as tabelas do banco de dados.
- `flask seed-db`: Limpa o banco de dados, adiciona produtos de exemplo e gera histórico de preços fictício.

Para listar todos os comandos disponíveis, use:

```
flask --help
```

### 8. Estrutura do docker-compose.yml

O arquivo `docker-compose.yml` define dois serviços:

- **app**: 
  - Constrói uma imagem Docker a partir do `Dockerfile` no diretório `backend/`.
  - Mapeia a porta `5000` do contêiner para a porta `5000` do host.
  - Define variáveis de ambiente para o Flask (`FLASK_APP`, `FLASK_ENV`) e Redis (`CACHE_REDIS_HOST`, `CACHE_REDIS_PORT`, `CACHE_REDIS_DB`, `CACHE_REDIS_URL`).
  - Monta o diretório `backend/` como um volume para refletir mudanças no código em tempo real.
  - Depende do serviço `redis`.

- **redis**:
  - Usa a imagem oficial `redis:7-alpine`.
  - Mapeia a porta `6379` do contêiner para a porta `6379` do host.

### 9. Configuração do Cache com Redis

O projeto utiliza o Flask-Caching com Redis para otimizar o desempenho da aplicação. As configurações incluem:

- Tipo de cache: `RedisCache`.
- Host: `redis` (nome do serviço no Docker Compose) ou `localhost` (para execução local).
- Porta: `6379`.
- Banco de dados: `0`.
- Tempo de expiração padrão: 5 minutos (300 segundos).

### 10. Solução de Problemas Comuns

- **Erro: "No module named 'app'"**:
  - Certifique-se de que está no diretório correto (`ecommerce/backend`) ou que o ambiente virtual está ativado com as dependências instaladas.
- **Erro ao acessar o banco de dados**:
  - Verifique se o arquivo `ecommerce.db` foi criado no diretório `backend/`.
  - Execute `flask init-db` para garantir que as tabelas estejam criadas.
- **Erro de conexão com o Redis**:
  - Confirme que o Redis está em execução (`redis-cli ping` deve retornar `PONG`).
  - No Docker, verifique se o serviço `redis` está ativo (`docker-compose ps`).
- **Docker não inicia**:
  - Verifique se o Docker está em execução (`docker ps`).
  - Certifique-se de que as portas `5000` e `6379` não estão em uso por outras aplicações.
- **Mudanças no código não refletem no contêiner**:
  - O volume mapeado no `docker-compose.yml` garante que as alterações no código sejam refletidas. Se isso não ocorrer, reconstrua a imagem com `docker-compose up --build`.

### 11. Dependências Principais

As principais dependências do projeto estão listadas em `requirements.txt`. Algumas delas incluem:

- Flask: Framework web para a API.
- Flask-SQLAlchemy: ORM para gerenciamento do banco de dados.
- Flask-CORS: Suporte a requisições cross-origin.
- Flasgger: Documentação automática da API com Swagger.
- Click: Para comandos CLI personalizados.
- Flask-Caching: Para integração com o Redis.
- redis: Cliente Python para comunicação com o Redis.

### 12. Automação de Preços

O projeto inclui um sistema de automação de preços que atualiza os preços dos produtos em intervalos regulares (a cada 10 segundos, por padrão). Isso é configurado no módulo `app.services.price_automation`. Os preços são armazenados no Redis para acesso rápido e registrados no banco de dados SQLite para histórico.

### 13. Testes Automatizados

Para realizar testes automatizados com o pytest, execute:

```
pytest app/tests/
```

Os testes unitários cobrem os modelos, endpoints da API e a lógica de automação de preços, garantindo a confiabilidade do backend.

### 14. Contribuindo

Se você deseja contribuir para o projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

### 15. Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Se precisar de mais ajuda, sinta-se à vontade para abrir uma issue no repositório!