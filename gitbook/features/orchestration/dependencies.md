# Dependency Resolution

How ByteClaude builds and validates the task dependency graph.

## Graph Construction

- Each task declares `dependencies: [ids]`
- Planner adds implicit deps (e.g., Setup → all)
- Topological sort orders tasks safely

## Cycle Detection

- Cycles are reported with the smallest offending loop
- Execution stops with an actionable message

## Best Practices

- Prefer fewer, meaningful dependencies
- Group logically related steps under a parent high-level task
- Use `--dry-run` to preview the DAG before executing


