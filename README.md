# ETL - Modelo Medalhão

<p align="center">
  <strong>Pipeline ETL completo implementando a arquitetura Medalhão (Bronze/Silver/Gold) com dados brasileiros.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Pandas-2.1-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-26-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

## Sobre o Projeto

O **ETL Medalhão** é uma solução completa de extração, transformação e carga de dados desenvolvida em Python. O sistema implementa a arquitetura Medallion (Bronze/Silver/Gold) para processar dados de usuários brasileiros, enriquecendo-os com informações de endereço completas via API ViaCEP. O pipeline garante qualidade de dados através de validações em múltiplas camadas, desde a ingestão bruta até a geração de datasets prontos para análise.

**Fluxo de Dados:**
```
80 usuários + 80 CEPs (Bronze - dados brutos)
         ↓
80 usuários + 58 CEPs válidos (Silver - dados limpos)
         ↓
62 usuários enriquecidos (Gold - dados para análise)
```

---

## Funcionalidades Principais

- **Extração de Dados (Bronze)**: Coleta dados brutos de arquivos CSV/JSON e API ViaCEP.
- **Transformação de Dados (Silver)**: Limpeza, validação e conversão para formato Parquet otimizado.
- **Carga de Dados (Load)**: Persistência dos dados no PostgreSQL com tipagem adequada.
- **Enriquecimento de Dados (Gold)**: Joins e agregações para gerar datasets prontos para análise/BI.
- **Arquitetura Modular**: Código organizado em camadas (`extract`, `transform`, `load`) para promover a separação de responsabilidades e fácil manutenção.
- **Ambiente Containerizado**: PostgreSQL totalmente gerenciado pelo Docker Compose, simplificando a configuração.

---

## Guia de Instalação e Execução

Para executar o projeto localmente, siga os passos abaixo.

### Pré-requisitos

- Python 3.12+
- Docker
- Docker Compose

### Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cauamapurunga/etl
   cd etl
   ```

2. **Configure o ambiente Python:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Inicie o banco de dados:**
   ```bash
   docker-compose up -d
   ```

4. **Execute o pipeline completo:**
   ```bash
   python run_etl.py
   ```

5. **Disponibilidade dos dados:**
   - **Bronze**: `data/01-bronze-raw/`
   - **Silver**: `data/02-silver-validated/`
   - **Gold**: `data/03-gold-enriched/`
   - **PostgreSQL**: `localhost:5432`

Para parar o banco de dados:
```bash
docker-compose down
```

---

## Documentação do Pipeline

### **Camada Bronze (Raw Data)**

Dados brutos extraídos sem nenhum tratamento, preservando a integralidade original para auditoria.

| Script | Descrição |
| :----- | :-------- |
| `scripts/extract/get_data.py` | Extrai CEPs de usuários e busca dados de endereço na API ViaCEP |

**O que faz:**
- Lê o arquivo `users.csv` com 80 usuários
- Para cada CEP, faz requisição à API ViaCEP
- A API retorna dados de endereço OU `{"erro": "true"}` quando o CEP é inválido/não encontrado
- Salva **todos** os resultados no CSV, preservando tanto sucessos quanto erros

**Dados gerados:**
- `users.csv`: 80 usuários com dados brasileiros (nome, email, telefone, CEP, nascimento, gênero)
- `cep_info.csv`: 80 registros totais (62 CEPs válidos + 18 com `erro: true`)

**Por que preservar erros?**
- Rastreabilidade: saber quais CEPs falharam
- Auditoria: histórico completo de todas as tentativas
- Debug: identificar padrões de falha na API

---

### **Camada Silver (Validated Data)**

Dados limpos, validados e convertidos para formato otimizado.

| Script | Descrição |
| :----- | :-------- |
| `scripts/transform/normalize_data.py` | Remove duplicatas, valida dados e converte para Parquet |

**O que faz:**
- Lê os 80 registros do Bronze (`cep_info.csv`)
- **Filtra e remove** linhas onde `erro == "true"` (CEPs que a API não encontrou)
- Remove a coluna `erro` (não é mais necessária após filtrar)
- Converte colunas com listas para strings
- Remove duplicatas completas
- Converte para formato Parquet (compressão e performance)

**Transformações aplicadas:**
- **Validação**: 80 → 58 registros CEP (removidos 18 com `erro: true` + 4 duplicatas)
- **Limpeza**: Remove coluna `erro` após filtrar
- **Otimização**: CSV → Parquet (~70% menor, 10x mais rápido)
- **Qualidade**: Apenas CEPs válidos e únicos

**Por que Parquet?**
- Compressão eficiente (economiza espaço)
- Leitura colunar rápida (perfeito para análises)
- Compatível com ferramentas Big Data (Spark, Athena, BigQuery)

---

### **Camada Load (Database)**

Carga dos dados validados no PostgreSQL para consultas relacionais.

| Script | Descrição |
| :----- | :-------- |
| `scripts/load/populate_db.py` | Cria tabelas e insere dados do Silver no PostgreSQL |

**O que faz:**
- Lê arquivos Parquet do Silver
- Cria tabelas automaticamente no PostgreSQL
- Insere dados com tipagem TEXT (flexível)
- Permite consultas SQL sobre os dados

**Tabelas criadas:**
- `users`: 80 usuários completos
- `cep_info`: 58 endereços válidos

**Por que carregar no banco?**
- Consultas SQL complexas (joins, agregações)
- Múltiplos usuários podem acessar
- Integração com ferramentas de BI

---

### **Camada Gold (Enriched Data)**

Dados enriquecidos prontos para análise e Business Intelligence.

| Script | Descrição |
| :----- | :-------- |
| `scripts/enrich/enrich_data.py` | Executa query SQL para juntar users + CEP e gera datasets finais |

**O que faz:**
- Executa INNER JOIN entre `users` e `cep_info` pelo campo CEP
- Combina dados pessoais com endereço completo
- Gera estatísticas descritivas (estados, gênero)
- Exporta em dois formatos: Parquet (análise) e CSV (visualização)

**Query executada:**
```sql
SELECT 
    users.id,
    users.nome,
    users.email,
    users.data_nascimento,
    users.genero,
    cep_info.logradouro,
    cep_info.localidade,
    cep_info.uf,
    cep_info.estado,
    cep_info.regiao
FROM users
INNER JOIN cep_info ON cep_info.cep = users.cep
ORDER BY id;
```

**Dados gerados:**
- `users_enriched.parquet`: 62 registros otimizados
- `users_enriched.csv`: 62 registros para análise

**Por que 62 registros?**
- 80 usuários iniciais
- 18 usuários têm CEPs com erro (removidos no Silver)
- Alguns CEPs aparecem em múltiplos usuários (ex: 2 pessoas na mesma rua)
- INNER JOIN garante apenas correspondências válidas

**Estatísticas:**
- 16 estados diferentes representados
- Distribuição equilibrada: 50% masculino, 50% feminino
- Cobertura nacional (Norte, Sul, Sudeste, Nordeste, Centro-Oeste)

---

## Estrutura do Projeto

O projeto segue uma arquitetura em camadas para promover a organização e o desacoplamento do código:

```
etl/
├── data/
│   ├── 01-bronze-raw/          # Dados brutos (CSV, JSON)
│   ├── 02-silver-validated/    # Dados limpos (Parquet)
│   └── 03-gold-enriched/       # Dados enriquecidos (análise)
├── scripts/
│   ├── extract/
│   │   └── get_data.py         # Extração de dados da API
│   ├── transform/
│   │   └── normalize_data.py   # Normalização e limpeza
│   ├── load/
│   │   └── populate_db.py      # Carga no PostgreSQL
│   └── enrich/
│       └── enrich_data.py      # Enriquecimento final (Gold)
├── config/
│   └── db.py                   # Conector do banco de dados
├── .gitignore
├── docker-compose.yml          # Orquestração do PostgreSQL
├── requirements.txt            # Dependências Python
├── run_etl.py                  # Orquestrador do pipeline
└── README.md                   # Este arquivo
```

---

## Tecnologias Utilizadas

- **Python 3.12**: Linguagem principal
- **Pandas 2.1**: Manipulação e análise de dados
- **PyArrow**: Suporte ao formato Parquet
- **Psycopg2**: Conector PostgreSQL
- **Requests**: Consumo da API ViaCEP
- **PostgreSQL 16**: Banco de dados relacional
- **Docker**: Containerização

---

## Estatísticas dos Dados

- **80 usuários** com dados demográficos brasileiros
- **62 usuários enriquecidos** com endereço completo
- **16 estados** representados
- **Distribuição equilibrada**: 50% masculino, 50% feminino

---

## Banco de Dados

**Configuração padrão:**

| Parâmetro | Valor |
| :-------- | :---- |
| Host | `localhost` |
| Porta | `5432` |
| Database | `postgres` |
| Usuário | `postgres` |
| Senha | `postgres` |

---

## Fluxo ETL

1. **Extract (Bronze)**: Busca CEPs dos usuários na API ViaCEP e salva dados brutos
2. **Transform (Silver)**: Limpa e converte dados para formato Parquet
3. **Load**: Insere dados validados no PostgreSQL
4. **Enrich (Gold)**: Gera datasets enriquecidos com joins e agregações

---

## Execução Individual das Etapas

Se preferir executar as etapas separadamente:

```bash
# Bronze: Extração
python scripts/extract/get_data.py

# Silver: Transformação
python scripts/transform/normalize_data.py

# Load: Carga no banco
python scripts/load/populate_db.py

# Gold: Enriquecimento
python scripts/enrich/enrich_data.py
```
