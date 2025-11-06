# Example: Data Pipeline

Daily ETL from Airtable → MongoDB → Excel Report.

```bash
python orchestrator/main.py --task "ETL: Airtable to MongoDB to Excel with charts" --output-dir ./output/etl
```

Outputs:
- MongoDB collection with normalized data
- XLSX report in `output/etl/`


