# ETL - Modelo Medalhão

Pipeline ETL completo implementando a arquitetura Medalhão (Bronze/Silver/Gold) com dados brasileiros.

## 📋 Estrutura do Projeto

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
│   └── load/
│       ├── populate_db.py      # Carga no PostgreSQL
│       └── enrich_gold.py      # Enriquecimento final
├── config/
│   └── db.py                   # Conector do banco de dados
├── run_etl.py                  # Orquestrador do pipeline
└── docker-compose.yml          # PostgreSQL containerizado
```

## 🎯 Camadas do Medalhão

### 🥉 Bronze (Raw Data)
- **Dados brutos** sem tratamento
- Origem: API ViaCEP, arquivos CSV/JSON
- Arquivos: `users.csv`, `products.json`, `cep_info.csv`

### 🥈 Silver (Validated Data)
- **Dados limpos** e validados
- Formato Parquet otimizado
- Remoção de duplicatas
- Conversão de tipos

### 🥇 Gold (Enriched Data)
- **Dados prontos** para análise/BI
- Join de users + endereços (CEP)
- Agregações e métricas

## 🚀 Como Executar

### Pré-requisitos
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Subir o banco de dados
```bash
docker-compose up -d
```

### Executar pipeline completo
```bash
python run_etl.py
```

### Executar etapas individuais
```bash
python scripts/extract/get_data.py        # Bronze: Extração
python scripts/transform/normalize_data.py  # Silver: Normalização
python scripts/load/populate_db.py     # Load: Carga no banco
python scripts/load/enrich_gold.py     # Gold: Enriquecimento
```

## 🛠️ Tecnologias

- **Python 3.12**
- **Pandas**: Manipulação de dados
- **Psycopg2**: Conector PostgreSQL
- **PyArrow**: Formato Parquet
- **Requests**: Consumo de API
- **PostgreSQL 16**: Banco de dados (Docker)

## 📊 Dados

- **80 usuários** com dados brasileiros
- **40 produtos** de diversas categorias
- **Endereços completos** via API ViaCEP
- **16 estados** diferentes

## 🗄️ Banco de Dados

**Host**: localhost  
**Porta**: 5432  
**Database**: postgres  
**User**: postgres  
**Password**: postgres

## 📝 Fluxo ETL

1. **Extract**: Busca CEPs na API ViaCEP
2. **Transform**: Limpa e converte para Parquet
3. **Load**: Insere dados no PostgreSQL
4. **Enrich**: Gera dados finais com joins e agregações
