# Skills System

Skills are reusable capability adapters (web, document, design, dev) the engine uses to generate or transform artifacts.

## Available Skills (Examples)

- Document: docx, pdf, pptx, xlsx
- Web: artifacts-builder (React/Vue components, dashboards)
- Design: theme-factory, canvas-design
- Dev: mcp-builder, skill-creator

## How It Works

1) Planner detects that a skill is needed (e.g., "create React component")
2) Engine loads the skill adapter and instructions
3) Adapter produces files (e.g., `.tsx`, `.css`, images) into workspace

## Configuration

- Skills catalog: `config/skills-manifest.yaml`
- Output directory: `execution.output_directory`

## Best Practices

- Start with minimal scope; iterate with additional tasks
- Combine with Context7 docs for current best practices
- Validate generated outputs and tests


