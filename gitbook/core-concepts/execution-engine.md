# Execution Engine

The orchestrator that turns plans into results.

## Responsibilities

- Execute tasks sequentially or in parallel
- Maintain shared `ExecutionContext`
- Manage retries and backoff
- Save checkpoints between tasks
- Emit progress and final reports

## ExecutionContext (simplified)

```python
work_directory: str
output_directory: str
project_variables: dict
cached_documentation: dict[str, str]
execution_results: dict[str, TaskResult]
```

## Lifecycle

1) Initialize context and directories
2) Validate dependencies for each task
3) Run tasks (async groups via `asyncio.gather()`)
4) Retry on retryable failures (max N)
5) Save checkpoints and update metrics
6) Validate outputs and generate documentation

## Error Handling

- RetryableError → retry with exponential backoff
- CriticalError → abort remaining tasks
- Non-critical → record warning and continue

## Reports

- `output/<project>/execution_report.json`
  - Tasks, durations, status
  - Errors/warnings
  - Success rate and totals

## Integration Points

- Skills Adapters (web, document, design, dev)
- MCP Handlers (MongoDB, Stripe, Notion, etc.)
- Context7 Client (library docs)

## Tuning

- Increase `framework.max_parallel_tasks` for speed
- Adjust `execution.max_retries` for flaky operations
- Disable non-critical validations during prototyping


