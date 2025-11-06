# Parallel Execution

Optimizing throughput while preserving dependency correctness.

## Strategy

- Identify independent tasks per level in the DAG
- Execute each level with a concurrency cap: `framework.max_parallel_tasks`
- Use async groups under the hood (`asyncio.gather`)

## Tuning

- Increase `max_parallel_tasks` to reduce wall time (CI/CD or powerful machines)
- Watch for external rate limits (Stripe/MongoDB) when increasing concurrency

## Metrics

- Per-task duration
- Group duration (dominant task)
- Total wall time vs. serial estimate


