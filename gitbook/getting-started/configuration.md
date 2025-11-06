# Configuration Guide

ByteClaude uses a 3-layer configuration system: Defaults ← Global (`config/`) ← CLI.

## Files

- `config/framework-config.yaml` – global defaults
- `mcp-registry.yaml` – MCP definitions and credentials keys
- `skills-manifest.yaml` – available skills list

## Merging Rules

- CLI flags override global config
- Global config overrides built-in defaults

## Example `framework-config.yaml`

```yaml
framework:
  max_parallel_tasks: 5
  enable_checkpoints: true

execution:
  work_directory: "./workspace"
  output_directory: "./output"
  continue_on_error: false
  max_retries: 3

context7:
  enabled: true
  cache_ttl: 3600

validation:
  run_tests: true
  code_review: true
  test_coverage_threshold: 80
```

## CLI Flags (Common)

```bash
python orchestrator/main.py \
  --task "Build a dashboard" \
  --dry-run \
  --include-tests \
  --output-dir ./output/my-app \
  --log-level DEBUG
```

## Environment Variables (`.env`)

```bash
NOTION_API_KEY=...
STRIPE_API_KEY=...
HUBSPOT_API_KEY=...
MONGODB_URI=mongodb://localhost:27017
BYTECLAUDE_LOG_LEVEL=INFO
```

Load via your shell or a dotenv loader. Secrets should not be stored in YAML.

## Context7 Library Mappings

`config/context7-library-mappings.yaml` powers library resolution:

```yaml
react: "/facebook/react"
next.js: "/vercel/next.js"
mongodb: "/mongodb/docs"
stripe: "/stripe/stripe-node"
```

## Profiles (Optional)

```yaml
environment: "production"

development:
  verbose_logging: true

production:
  enable_monitoring: true
```

## Validation Controls

```yaml
validation:
  run_tests: true
  code_review: true
  test_coverage_threshold: 80
```

Disable temporarily via CLI `--skip-tests` if supported.

## Tips

- Keep secrets in env vars
- Use `--dry-run` to validate config
- Prefer descriptive output directories per project


