# Execution Engine API

Interfaces to orchestrate and observe task execution.

## Core

```python
async def execute_plan(plan: ExecutionPlan) -> ExecutionResults: ...
def execute_task(task: Task) -> TaskResult: ...
```

## Context

```python
class ExecutionContext:
    work_directory: str
    output_directory: str
    project_variables: dict
    cached_documentation: dict
    execution_results: dict[str, TaskResult]
```

## Errors

- RetryableError
- CriticalError


