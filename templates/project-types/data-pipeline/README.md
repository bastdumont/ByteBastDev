# Python Data Pipeline

ETL data pipeline with Apache Airflow, dbt, and PostgreSQL.

## Overview

Complete data pipeline featuring:
- **Apache Airflow**: Workflow orchestration
- **dbt**: Data transformation
- **PostgreSQL**: Data warehouse
- **Pandas**: Data processing
- **Logging**: Pipeline monitoring

## Features

✅ **Airflow**
- DAG orchestration
- Scheduling
- Monitoring
- Error handling

✅ **dbt**
- SQL transformations
- Data lineage
- Testing
- Documentation

✅ **Warehousing**
- PostgreSQL
- Incremental models
- Aggregations

✅ **Monitoring**
- Logs
- Metrics
- Alerts

## Quick Start

### Prerequisites
```bash
Python >= 3.11
PostgreSQL >= 14
```

### Installation

```bash
pip install -r requirements.txt
airflow db init
airflow webserver &
airflow scheduler
```

### Access
- Airflow UI: http://localhost:8080

## Project Structure

```
data-pipeline/
├── dags/                 # Airflow DAGs
├── dbt/
│   ├── models/          # SQL models
│   ├── tests/           # Data tests
│   └── dbt_project.yml  # Config
├── scripts/             # Python scripts
└── README.md
```

---

**Build powerful data pipelines!** 📊
