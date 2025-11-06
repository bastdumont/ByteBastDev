# Task Orchestration

ByteClaude orchestrates independent and dependent tasks with robust error handling.

## Highlights

- Dependency-aware scheduling (topological)
- Parallel groups with configurable concurrency
- Checkpoints for resumable runs
- Structured reports and metrics

## Scheduling Model

```
Group 1: tasks with no deps → run in parallel
Group 2: tasks unblocked by Group 1 → run in parallel
...
```

The engine respects dependencies and `framework.max_parallel_tasks`.

## Failure Policy

- Critical tasks stop the pipeline
- Non-critical tasks record warnings and proceed
- Retries with exponential backoff for transient errors

## Observability

- Execution report with task-level metrics
- Optional monitoring dashboard (advanced features)


