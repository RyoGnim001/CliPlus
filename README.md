# CliPlus — Sistema de Registro de Consultas

API para gerenciamento de consultas de clínica médica, desenvolvida com ApiFlask e Supabase.

## Tecnologias

- **Python** com **ApiFlask** — framework web para a API REST
- **Supabase** — banco de dados PostgreSQL + autenticação
- **ReportLab** — geração de comprovantes em PDF
- **Gmail SMTP** — envio de comprovantes por email
- **uv** — gerenciador de pacotes

## Estrutura do projeto

```
CliPlus/
├── app/
│   ├── database/
│   │   └── supabase_client.py      # conexão com o Supabase
│   ├── helpers/
│   │   └── auth.py                 # autenticação via JWT
│   ├── models/                     # modelos de dados
│   ├── repository/
│   │   ├── consultas_repository.py # queries de consultas
│   │   └── pacientes_repository.py # queries de pacientes
│   ├── routes/
│   │   ├── comprovante.py          # endpoint de comprovante PDF
│   │   ├── consultas.py            # endpoints de consultas
│   │   ├── me.py                   # endpoint do operador logado
│   │   └── pacientes.py            # endpoint de pacientes
│   ├── schemas/
│   │   ├── consulta_schema.py      # validação de consulta
│   │   └── paciente_schema.py      # validação de paciente
│   ├── services/
│   │   ├── comprovante_service.py  # geração de PDF
│   │   ├── consultas_service.py    # lógica de negócio de consultas
│   │   ├── email_service.py        # envio de email
│   │   └── pacientes_service.py    # lógica de negócio de pacientes
│   └── templates/
│       ├── img/
│       │   └── logo.png            # logo da clínica
│       └── comprovante.html        # template do comprovante
├── settings/
│   └── config.py                   # variáveis de ambiente
├── .env                            # credenciais (não versionar)
├── .gitignore
├── main.py                         # inicialização da aplicação
└── pyproject.toml
```

## Instalação

**1. Clone o repositório:**
```bash
git clone https://github.com/RyoGnim001/CliPlus.git
cd CliPlus
```

**2. Instale as dependências:**
```bash
uv sync
```

**3. Configure as variáveis de ambiente:**

Solicite o arquivo `.env` ao administrador do projeto e coloque na raiz.

**4. Inicie o servidor:**
```bash
uv run python main.py
```

A API estará disponível em `http://localhost:5000`.
A documentação interativa estará em `http://localhost:5000/docs`.

## Endpoints

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `GET` | `/health` | Verifica se a API está online | Não |
| `GET` | `/me` | Dados do operador logado | Sim |
| `GET` | `/pacientes/{cpf}` | Busca paciente por CPF | Sim |
| `POST` | `/consultas` | Registra nova consulta | Sim |
| `GET` | `/consultas` | Lista todas as consultas | Sim |
| `GET` | `/consultas/{id}` | Detalhes de uma consulta | Sim |
| `GET` | `/consultas/{id}/comprovante` | Gera PDF do comprovante | Sim |

## Autenticação

A autenticação é feita via **Supabase Auth** com email e senha. O token JWT deve ser enviado no header de todas as requisições protegidas:

```
Authorization: Bearer SEU_TOKEN_JWT
```

## Fluxo principal

```
Operador loga no sistema
        ↓
Digita CPF do paciente no formulário
        ↓
GET /pacientes/{cpf}
  → paciente existe: preenche campos automaticamente
  → paciente não existe: operador preenche manualmente
        ↓
Operador preenche dados da consulta e salva
        ↓
POST /consultas:
  → cria paciente se não existir (deduplicação por CPF)
  → registra a consulta
  → gera PDF do comprovante
  → envia comprovante por email para o paciente
```

## Adicionando um novo operador

Os operadores são cadastrados manualmente pelo admin — sem fluxo de signup.

**1. Crie o usuário no Supabase Auth:**
- Acesse **Authentication → Users → Add user → Create new user**
- Preencha email e senha do operador
- Marque **Auto Confirm User** e clique em **Create**
- Copie o UUID gerado

**2. Vincule na tabela usuarios:**

```sql
INSERT INTO usuarios (auth_uid, email, nome, ativo)
VALUES ('uuid-copiado', 'email@clinica.com', 'Nome do Operador', TRUE);
```

**3. Entregue as credenciais** (email + senha) para o operador usar na tela de login.

## Redefinindo senha de um operador

```sql
UPDATE auth.users
SET encrypted_password = crypt('nova_senha', gen_salt('bf'))
WHERE email = 'email@clinica.com';
```

## Clínica

**Clínica Saúde & Vida**
Rua Coronel Adauto, 142 — Centro
Guarabira — PB, 58200-000
CNPJ: 12.345.678/0001-99
