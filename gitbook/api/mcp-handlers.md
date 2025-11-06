# MCP Handlers API

Common capabilities and patterns for handlers (MongoDB, Stripe, Notion, etc.).

## Interface (Conceptual)

```python
class Handler:
    async def connect(self) -> bool: ...
    async def close(self) -> None: ...
```

Handlers also expose domain-specific methods (e.g., `find`, `insert`).

## Error Handling

- Transient errors → retries with backoff
- Permanent errors → surfaced to engine


