# Creating Skills

Add a new skill adapter for artifact generation.

## Steps

1) Register skill in `skills-manifest.yaml`
2) Implement adapter with `load(config)` and `execute(instructions)`
3) Write outputs to `execution.output_directory`
4) Add documentation and examples

## Tips

- Keep adapters stateless where possible
- Return produced file paths for traceability


