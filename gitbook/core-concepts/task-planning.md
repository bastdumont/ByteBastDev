# Task Planning Engine

How natural language becomes an optimized execution plan.

## Responsibilities

- Analyze request text and extract technologies/constraints
- Map technologies → MCPs, Skills, Context7 libraries
- Decompose into tasks with priorities and estimates
- Build dependency graph and detect cycles
- Optimize parallel groups within `max_parallel_tasks`

## Flow

```
Input → analyze_request() → create_execution_plan() → optimize_plan()
```

Example output (simplified):

```
Tasks:
1) Setup (critical)
2) Fetch Docs (depends: 1)
3) Generate App (depends: 1,2)
4) Integrate Services (depends: 3)
5) Tests (depends: 3,4)
6) Validate & Docs (depends: all)
```

## Technology Detection

- Keywords → MCPs (e.g., "stripe" → Stripe MCP)
- Keywords → Skills (e.g., "react" → artifacts-builder)
- Keywords → Context7 docs (e.g., React, Next.js, MongoDB)

## Dependency Resolution

- Topological sort
- Cycle detection with clear errors
- Guard rails to prevent orphaned tasks

## Parallel Optimization

- Group tasks without dependency conflicts
- Bound concurrency by `framework.max_parallel_tasks`
- Recalculate duration using group maxima

## Configuration Knobs

- `framework.max_parallel_tasks`
- `execution.max_retries`
- `validation.*`

## Error Handling

- Mark critical failures to stop the pipeline (e.g., setup failure)
- Non-critical issues (e.g., optional docs) allow continuation

## Extending Planning Logic

- Update tech→MCP/Skill maps
- Add new task types and planner rules
- Enhance heuristics for estimates/priorities


