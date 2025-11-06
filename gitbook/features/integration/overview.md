# Integration Layer Overview

Seamless access to external systems via MCP Handlers, Skills, and Context7.

## Components

- MCP Handlers: Database, payment, productivity, web tools
- Skills Adapters: Web, document, design, dev capabilities
- Context7 Client: Real-time library documentation

## Typical Flow

1) Planner detects technology needs from your request
2) Maps to MCPs/Skills and relevant documentation
3) Engine invokes handlers/adapters with retries and metrics

## Supported Categories

- Databases: MongoDB, Airtable
- Payments: Stripe
- Productivity: Notion, HubSpot
- System: Filesystem, Chrome
- Web: Search, Fetch
- Docs: Context7

Configure credentials via environment variables and `mcp-registry.yaml`.


