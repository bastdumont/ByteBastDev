# FastAPI Template

Modern Python API starter with health checks and metrics.

## Features

- `/health` and `/metrics` endpoints
- Structured project layout
- Ready for uvicorn

## Getting Started

```bash
python orchestrator/main.py --task "Create FastAPI backend" --output-dir ./output/fastapi
cd output/fastapi
pip install -r requirements.txt
uvicorn app.main:app --reload
```


