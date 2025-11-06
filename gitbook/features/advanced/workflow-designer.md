# Workflow Designer

Design, preview, and execute complex workflows via a higher-level interface.

## Capabilities

- Define multi-stage workflows with dependencies
- Parameterize steps and share variables
- Preview plans before execution
- Export/import workflow definitions

## Example

```yaml
name: saas-onboarding
steps:
  - id: setup
    task: "Initialize monorepo and environment"
  - id: backend
    depends_on: [setup]
    task: "Create FastAPI backend with /auth and /metrics"
  - id: frontend
    depends_on: [setup]
    task: "Create Next.js app with login page"
  - id: integration
    depends_on: [backend, frontend]
    task: "Wire auth endpoints and session handling"
```

## Usage

- Preview only: `--dry-run`
- Execute: `python orchestrator/main.py --task "..."`


