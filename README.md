# Aplicação Full-Stack com React, Flask e Redis

Este é um projeto full-stack com um frontend construído em [React](https://react.dev/) usando [Vite](https://vitejs.dev/) e um backend em [Flask](https://flask.palletsprojects.com/) com cache em [Redis](https://redis.io/). A aplicação é orquestrada usando [Docker Compose](https://docs.docker.com/compose/).

## Estrutura do Projeto

- `frontend/` - Código do frontend (React com Vite).
- `backend/` - Código do backend (Flask com Redis para cache).
- `docker-compose.yml` - Arquivo de configuração para orquestrar os serviços.
- `README.md` - Este arquivo com instruções.

## Pré-requisitos

Certifique-se de ter instalado:

- [Docker](https://www.docker.com/get-started) (versão mais recente)
- [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído com o Docker Desktop)

## Configuração

1. Clone este repositório:

   ```bash
   git clone https://github.com/joelvitorniino/ecommerce-price-automation/
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd ecommerce-price-automation
   ```

## Rodando a Aplicação

Para iniciar todos os serviços (frontend, backend e Redis) usando Docker Compose:

```bash
docker-compose up --build
```

Isso irá:
- Construir as imagens Docker para o frontend e backend.
- Iniciar o Redis usando a imagem oficial `redis:7-alpine`.
- Expor as portas:
  - Frontend: `http://localhost:3000`
  - Backend: `http://localhost:8000`
  - 
Para rodar em modo detached (em segundo plano):

```bash
docker-compose up --build -d
```

## Acessando a Aplicação

- **Frontend**: Acesse `http://localhost:3000` no navegador.
- **Backend**: A API estará disponível em `http://localhost:8000`.
- **Redis**: Conecte-se ao Redis na porta `6379` (se necessário, usando um cliente como `redis-cli`).

## Parando a Aplicação

Para parar os serviços:

```bash
docker-compose down
```

Para remover os volumes e limpar completamente:

```bash
docker-compose down -v
```

## Estrutura dos Serviços

- **Frontend**:
  - Construído com Vite e React.
  - Roda em `NODE_ENV=production`.
  - Exposto na porta `3000`.
  - Depende do backend para chamadas de API.

- **Backend**:
  - Construído com Flask.
  - Configurado com `FLASK_ENV=development` para desenvolvimento.
  - Usa Redis para cache, configurado via variáveis de ambiente.
  - Exposto na porta `8000`.
  - Monta o diretório `./backend` como volume para desenvolvimento.

- **Redis**:
  - Usa a imagem oficial `redis:7-alpine`.
  - Exposto na porta `6379` para conexões locais (opcional).

## Desenvolvimento

- **Frontend**:
  - Edite os arquivos em `./frontend`.
  - O Vite suporta hot-reload em desenvolvimento (se configurado no Dockerfile do frontend).

- **Backend**:
  - Edite os arquivos em `./backend`.
  - Alterações são refletidas automaticamente devido ao volume montado.

## Build para Produção

Os serviços já estão configurados para produção no `docker-compose.yml`:
- Frontend usa `NODE_ENV=production`.
- Backend usa Flask com Redis para cache otimizado.

Para builds manuais (sem Docker):
- **Frontend**: Navegue até `./frontend` e execute `npm run build` (ou `yarn build`).
- **Backend**: Certifique-se de que o Redis está rodando e execute `flask run` em `./backend`.

## Solução de Problemas

- **Portas ocupadas**: Verifique se as portas `3000`, `8000` ou `6379` estão livres.
- **Erros de build**: Confirme que os Dockerfiles em `./frontend` e `./backend` estão corretos.
- **Conexão com Redis**: Certifique-se de que o serviço `redis` está ativo antes do backend.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Faça o push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
