# SIG Scraper API

API REST para download automatizado de notas fiscais do sistema SIGAR Aguaia.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python (instaladas automaticamente via requirements.txt):
  - Flask
  - requests
  - Werkzeug

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando a API

Para iniciar o servidor da API:

```bash
python app.py
```

Por padrão, a API estará disponível em `http://localhost:5000`

## Endpoints

### POST /download_notas

Endpoint para download de notas fiscais em formato ZIP.

#### Parâmetros (JSON)

- `cnpj` (obrigatório): CNPJ para login
- `senha` (obrigatório): Senha para login
- `data_inicio` (opcional): Data de início no formato DD/MM/AAAA (padrão: 01/03/2025)
- `data_fim` (opcional): Data de fim no formato DD/MM/AAAA (padrão: 31/03/2025)

#### Exemplo de requisição

```bash
curl -X POST http://localhost:5000/download_notas \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "seucnpj",
    "senha": "SuaSenha",
    "data_inicio": "01/01/2024",
    "data_fim": "31/01/2024"
  }' \
  --output notas.zip
```

#### Respostas

- **200 OK**: Retorna o arquivo ZIP com as notas fiscais
- **400 Bad Request**: CNPJ ou senha não fornecidos
- **401 Unauthorized**: Falha no login (credenciais inválidas)
- **500 Internal Server Error**: Erro ao pesquisar notas ou gerar ZIP

## Notas

- O ViewState utilizado nas requisições pode expirar ou mudar com o tempo. Se ocorrerem erros, pode ser necessário atualizar esse valor no código.
- Os arquivos são temporariamente salvos no diretório temporário do sistema antes de serem enviados como resposta.
- A API usa HTTPS para garantir a segurança das credenciais durante a transmissão. 