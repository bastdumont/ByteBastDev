# Skills API

Capabilities for artifact generation and transformation.

## Interface (Conceptual)

```python
class SkillAdapter:
    def load(self, config: dict) -> None: ...
    def execute(self, instructions: dict) -> list[str]: ...  # returns file paths
```

## Outputs

- Files written under `execution.output_directory`
- Logs and metadata for reproducibility


