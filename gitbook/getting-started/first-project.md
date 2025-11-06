# Your First Project

Build and ship your first ByteClaude project in 10–20 minutes.

## Goal

- Create a React dashboard with API integration
- Generate tests and documentation
- Inspect outputs and iterate

## Prerequisites

- Python 3.8+
- pip
- (Optional) Node.js 18+ for frontend templates

## 1) Describe What To Build

```bash
python orchestrator/main.py \
  --task "Create a React dashboard with a table, chart, and mocked API" \
  --output-dir ./output/react-dashboard
```

What happens:
- Planner analyzes the request and detects: React, charts, API
- Context7 docs fetched (React, Tailwind)
- Tasks are generated and executed in parallel where possible

## 2) Inspect Outputs

```
output/react-dashboard/
├── README.md
├── execution_report.json
├── src/
│   ├── App.tsx
│   ├── components/
│   └── services/
└── tests/
```

Quick checks:
- Open `execution_report.json` to review tasks, durations, and errors
- Read `README.md` for local run instructions

## 3) Run Locally (Frontends)

```bash
cd output/react-dashboard
npm install
npm run dev
```

Then visit `http://localhost:5173` (or the port shown by Vite/Next.js).

## 4) Add a Feature (Iterate)

Describe additions incrementally:

```bash
python orchestrator/main.py \
  --task "Add filtering and CSV export to the dashboard table" \
  --output-dir ./output/react-dashboard
```

The engine will plan minimal changes and update the workspace.

## 5) Generate Tests

```bash
python orchestrator/main.py \
  --task "Generate tests for table filtering and chart rendering" \
  --include-tests \
  --output-dir ./output/react-dashboard
```

Where tests go:
- `tests/` for Python/Node test suites
- Reports captured in `execution_report.json`

## 6) Backend Example (FastAPI)

```bash
python orchestrator/main.py \
  --task "Create a FastAPI backend with health endpoint and /metrics" \
  --output-dir ./output/fastapi-backend

cd output/fastapi-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Endpoints to try:
- GET `/health` → `{ "status": "healthy" }`
- GET `/metrics` → demo metrics payload

## 7) Full-Stack Example

```bash
python orchestrator/main.py \
  --task "Create full-stack app: Next.js frontend + FastAPI backend + MongoDB" \
  --include-tests \
  --output-dir ./output/fullstack
```

Outputs:
- `frontend/` → Next.js app
- `backend/` → FastAPI app
- `.env.example` files for configuration

## 8) Troubleshooting

- Use `--dry-run` to preview a plan without executing
- Increase logs: `--log-level DEBUG`
- Rerun failed steps; checkpoints resume from last success

## 9) Next Steps

- Explore templates in `templates/project-types/`
- Read the architecture deep dive at `core-concepts/architecture.md`
- Enable MCPs (Stripe, MongoDB) for integrations


