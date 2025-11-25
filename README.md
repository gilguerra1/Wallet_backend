# Wallet API

API para gerenciamento de carteiras digitais com suporte a múltiplas moedas (cripto e fiat), depósitos, saques, conversões e transferências entre carteiras.

## Funcionalidades

- **Mini-Sprint 1**: Criação de carteiras
- **Mini-Sprint 2**: Consulta de saldos
- **Mini-Sprint 3**: Depósitos e saques
- **Mini-Sprint 4**: Conversão de moedas (integração com API Coinbase)
- **Mini-Sprint 5**: Transferências entre carteiras

## Tecnologias

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- Docker & Docker Compose

## Pré-requisitos

### Com Docker
- Docker
- Docker Compose

### Sem Docker
- Python 3.11+
- PostgreSQL 15+
- pip

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_DRIVER=
PRIVATE_KEY_SIZE=
PUBLIC_KEY_SIZE=
TAXA_SAQUE_PERCENTUAL=
TAXA_CONVERSAO_PERCENTUAL=
TAXA_TRANSFERENCIA_PERCENTUAL=
COINBASE_API_BASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

### CORS / ALLOWED_ORIGINS

Se você estiver desenvolvendo o frontend localmente em outra origem (por exemplo `http://localhost:3000`), o navegador pode bloquear chamadas para a API por causa da política CORS. Para permitir essas origens durante desenvolvimento, adicione a variável `ALLOWED_ORIGINS` no arquivo `.env` com uma lista separada por vírgulas de origens permitidas (ex.: `http://localhost:3000,http://localhost:5500`).

Exemplo:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5500
```

No ambiente de produção prefira listar explicitamente os domínios confiáveis ou gerenciar CORS em um proxy reverso / gateway.

## Executando o Projeto

### Opção 1: Com Docker (Recomendado)

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd backend
```

2. **Inicie os containers:**
```bash
docker-compose up -d
```

3. **Verifique os logs:**
```bash
docker-compose logs -f app
```

4. **Acesse a API:**
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs
- Banco de dados: localhost:5432

5. **Parar os containers:**
```bash
docker-compose down
```

6. **Rebuild após alterações:**
```bash
docker-compose up -d --build
```

### Opção 2: Sem Docker (Local)

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd backend
```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o PostgreSQL:**
- Instale o PostgreSQL 15+
- Crie o banco de dados:
```sql
CREATE DATABASE wallet_api_homolog;
```

5. **Execute as migrations:**
```bash
alembic upgrade head
```

6. **Inicie o servidor:**
```bash
uvicorn main:app --reload
```

7. **Acesse a API:**
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/V1/          # Routers (endpoints)
│   ├── core/            # Configurações
│   ├── models/          # Modelos Pydantic
│   ├── repositories/    # Acesso ao banco
│   └── services/        # Lógica de negócio
├── database/            # Configuração do banco
├── migrations/          # Migrations Alembic
├── .env                 # Variáveis de ambiente
├── main.py              # Entrada da aplicação
├── requirements.txt     # Dependências
├── Dockerfile           # Imagem Docker
└── docker-compose.yml   # Orquestração
```

## Endpoints Principais

### Carteiras
- `POST /api/v1/wallets` - Criar carteira
- `GET /api/v1/wallets/{address}` - Consultar carteira
- `GET /api/v1/wallets/{address}/balances` - Consultar saldos

### Depósitos e Saques
- `POST /api/v1/wallets/{address}/deposits` - Fazer depósito
- `POST /api/v1/wallets/{address}/withdrawals` - Fazer saque

### Conversões
- `POST /api/v1/wallets/{address}/conversions` - Converter moeda

### Transferências
- `POST /api/v1/carteiras/{endereco_origem}/transferencias` - Transferir entre carteiras

## Migrations

### Criar nova migration:
```bash
alembic revision -m "descrição"
```

### Aplicar migrations:
```bash
alembic upgrade head
```

### Reverter migration:
```bash
alembic downgrade -1
```

## Testes

Para testar os endpoints, use a documentação interativa em:
```
http://localhost:8000/docs
```

### Exemplo de Requisição - Criar Carteira:
```bash
curl -X POST http://localhost:8000/api/v1/wallets
```

### Exemplo de Requisição - Transferência:
```bash
curl -X POST http://localhost:8000/api/v1/carteiras/{endereco_origem}/transferencias \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_target_address": "endereço_destino",
    "currency_id": 1,
    "value": 100.00,
    "private_key": "sua_chave_privada"
  }'
```

## Taxas

- **Depósito**: 0%
- **Saque**: 1% (configurável)
- **Conversão**: 2% (configurável)
- **Transferência**: 1.5% (configurável)

## Moedas Suportadas

- BTC (Bitcoin)
- ETH (Ethereum)
- SOL (Solana)
- USD (US Dollar)
- BRL (Real Brasileiro)

## Troubleshooting

### Erro de conexão com banco de dados
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `.env`
- Com Docker: use `DB_HOST=db`
- Sem Docker: use `DB_HOST=localhost`

### Erro ao executar migrations
```bash
# Resete o Alembic
alembic stamp head
alembic upgrade head
```

### Porta já em uso
```bash
# Altere a porta no docker-compose.yml ou ao executar uvicorn
uvicorn main:app --port 8001
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é de uso educacional.
