# Example: API Integration

Connect to Stripe and Notion to orchestrate workflows.

```bash
python orchestrator/main.py --task "Sync Notion database to MongoDB and create Stripe invoices" --output-dir ./output/integration
```

Tips:
- Set API keys via environment variables
- Review `execution_report.json` for operation details


