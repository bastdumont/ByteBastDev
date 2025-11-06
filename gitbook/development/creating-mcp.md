# Creating MCP Handlers

Implement a new integration following the handler contract.

## Steps

1) Define configuration in `mcp-registry.yaml`
2) Implement async connect/close and domain methods
3) Add retries for transient failures
4) Register in Execution Engine handler registry

## Testing

- Mock external APIs
- Add integration tests when feasible


