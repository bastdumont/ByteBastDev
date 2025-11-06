# MCP Handlers

Model Context Protocol (MCP) handlers encapsulate external integrations with a consistent async API.

## Capabilities (Examples)

- MongoDB: connect, find/insert/update/delete, aggregate, indexes
- Stripe: customers, products, prices, invoices, refunds, subscriptions
- Notion: pages, databases, blocks, search
- Airtable: bases, tables, records
- HubSpot: contacts, companies, deals
- Filesystem: secure file and directory operations
- Chrome: navigation, scripting, screenshots
- Web Tools: search, fetch, scrape

## Configuration

Set credentials via env vars and reference in `mcp-registry.yaml`.

```yaml
stripe:
  api_key_env: STRIPE_API_KEY
mongodb:
  uri_env: MONGODB_URI
```

## Usage (Framework-Managed)

The Execution Engine instantiates handlers on demand, manages retries, and collects metrics. You typically just describe the task; orchestration selects and executes the right MCPs.

## Reliability

- Async I/O
- Exponential backoff on transient failures
- Structured error reporting


