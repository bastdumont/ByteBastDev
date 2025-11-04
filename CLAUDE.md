# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Automated Development Framework** that orchestrates Claude Code with Skills, MCPs (Model Context Protocol), and Context7 to enable natural language software development. The framework:
- Converts natural language requests into structured execution plans
- Orchestrates 15+ external integrations (MongoDB, Stripe, Notion, Airtable, HubSpot, etc.)
- Fetches real-time library documentation via Context7
- Executes tasks in parallel with dependency resolution
- Generates complete applications with tests and documentation

## Essential Commands

### Setup and Installation
```bash
# Initial setup (creates directories, installs dependencies, verifies config)
python setup.py

# Install dependencies manually
pip install -r requirements.txt
```

### Running the Framework
```bash
# Interactive mode (recommended for exploration)
python orchestrator/main.py
# or from root:
python main.py

# Single task execution
python orchestrator/main.py --task "Create a React dashboard with MongoDB"

# Dry run (show plan without executing)
python orchestrator/main.py --task "Build Next.js app" --dry-run

# With custom output directory
python orchestrator/main.py --task "Build app" --output-dir ./my-app

# Include test generation
python orchestrator/main.py --task "Build API" --include-tests

# Custom configuration
python orchestrator/main.py --config ./my-config.yaml --task "..."

# View help
python orchestrator/main.py --help
```

### Development Commands
```bash
# Test task planner standalone
python task_planner.py

# Test execution engine standalone
python execution_engine.py

# Check framework version
python orchestrator/main.py --version
```

## Architecture

### Core Components

1. **Task Planner** ([task_planner.py](task_planner.py))
   - Analyzes natural language requests
   - Detects technologies and maps to MCPs/Skills
   - Decomposes into structured tasks with dependencies
   - Optimizes execution order and identifies parallel groups
   - Key class: `TaskPlanner`

2. **Execution Engine** ([execution_engine.py](execution_engine.py))
   - Orchestrates task execution (sequential or parallel)
   - Manages Skills and MCP handlers
   - Tracks execution state and results
   - Handles errors with retry logic
   - Key class: `ExecutionEngine`

3. **Main CLI** ([main.py](main.py))
   - Command-line interface
   - Interactive and single-task modes
   - Configuration loading and merging
   - Key function: `main()`

### Task Flow

```
Natural Language Request
    ↓
TaskPlanner.analyze_request()
    ↓
TaskPlanner.create_execution_plan()
    ↓
TaskPlanner.optimize_plan()
    ↓
ExecutionEngine.execute_plan()
    ↓
Results + Execution Report
```

### Task Types (TaskType enum)
- `FILE_OPERATION`: Project setup, file creation
- `CODE_GENERATION`: Code generation tasks
- `WEB_DEVELOPMENT`: Web application development
- `DOCUMENT_GENERATION`: Document creation (docx, pdf, pptx, xlsx)
- `API_INTEGRATION`: External API integrations
- `DATABASE_OPERATION`: Database operations
- `TESTING`: Test generation and execution
- `VALIDATION`: Validation and documentation
- `DATA_PROCESSING`: Data pipeline tasks
- `DEPLOYMENT`: Deployment tasks

### Execution Statuses (ExecutionStatus enum)
- `PENDING`: Task not started
- `IN_PROGRESS`: Currently executing
- `COMPLETED`: Successfully completed
- `FAILED`: Execution failed
- `SKIPPED`: Skipped due to failed dependencies

## MCP Integration

Available MCPs are defined in [mcp-registry.yaml](mcp-registry.yaml):

**Databases**: mongodb, airtable
**Payment**: stripe
**Productivity**: notion, hubspot
**System**: filesystem, chrome, mac_control
**Documentation**: context7
**Media**: youtube
**Web**: web_search, web_fetch
**Communication**: beeper

Each MCP has registered handlers in `ExecutionEngine._register_mcp_handlers()` at [execution_engine.py:108](execution_engine.py#L108).

## Skills Integration

Skills are located at `/mnt/skills/` and include:
- **Documents**: docx, pdf, pptx, xlsx
- **Web**: artifacts-builder
- **Design**: theme-factory, canvas-design
- **Dev**: mcp-builder, skill-creator

Each skill has registered handlers in `ExecutionEngine._register_skill_handlers()` at [execution_engine.py:94](execution_engine.py#L94).

## Configuration

Main configuration file: `config/framework-config.yaml` (or `./mcp-registry.yaml` in root)

Key configuration sections:
- `framework.max_parallel_tasks`: Max concurrent tasks (default: 5)
- `execution.work_directory`: Working directory for builds (default: `./workspace`)
- `execution.output_directory`: Output directory (default: `./output`)
- `context7.enabled`: Enable Context7 documentation retrieval
- `context7.cache_ttl`: Documentation cache lifetime in seconds
- `validation.run_tests`: Auto-generate tests

Configuration is loaded and merged in [main.py:34](main.py#L34) using `load_config()`.

## Key Code Patterns

### Adding New Task Types

1. Add new `TaskType` enum value in [task_planner.py:13](task_planner.py#L13)
2. Add handler method in `ExecutionEngine` (e.g., `_execute_new_type`)
3. Route to handler in `ExecutionEngine.execute_task()` at [execution_engine.py:245](execution_engine.py#L245)
4. Update `_generate_tasks()` in TaskPlanner to create new task type

### Adding New MCP Handlers

1. Add MCP definition to [mcp-registry.yaml](mcp-registry.yaml)
2. Create handler method in `ExecutionEngine` (e.g., `_execute_new_mcp`)
3. Register handler in `_register_mcp_handlers()` at [execution_engine.py:108](execution_engine.py#L108)

### Adding New Skill Handlers

1. Ensure skill exists at `/mnt/skills/public/<skill-name>/SKILL.md`
2. Create handler method in `ExecutionEngine` (e.g., `_execute_new_skill`)
3. Register handler in `_register_skill_handlers()` at [execution_engine.py:94](execution_engine.py#L94)

### Technology Detection

Technology → MCP/Skill mapping in [task_planner.py:167-216](task_planner.py#L167-L216):
- `tech_mcp_mapping`: Maps keywords to MCPs (e.g., 'stripe' → stripe MCP)
- `tech_skill_mapping`: Maps keywords to Skills (e.g., 'react' → artifacts-builder)
- `context7_mapping`: Maps keywords to Context7 library IDs

To add new technology detection, update these mappings in `TaskPlanner.analyze_request()`.

### Dependency Resolution

Dependencies are resolved using topological sort in [task_planner.py:458](task_planner.py#L458) (`_resolve_dependencies()`).

Tasks specify dependencies via `Task.dependencies` (list of task IDs). The execution engine checks dependencies are satisfied before executing at [execution_engine.py:236](execution_engine.py#L236) (`_check_dependencies()`).

### Parallel Execution

Parallel execution is optimized in [task_planner.py:492](task_planner.py#L492) (`optimize_plan()`):
- Groups tasks without dependency conflicts
- Respects `max_parallel_tasks` configuration
- Recalculates duration based on parallel groups
- Executes groups via `asyncio.gather()` at [execution_engine.py:217](execution_engine.py#L217)

## Important Constraints

- **Skills directory**: `/mnt/skills/` (public and examples subdirectories)
- **Docker requirement**: MongoDB, Stripe, Notion, YouTube MCPs require Docker
- **Work directory structure**: `./workspace/<project_name>/`
- **Output directory structure**: `./output/<project_name>/`
- **Python version**: 3.8+ required
- **Async pattern**: Use `asyncio.run()` or `await` for execution engine methods

## Execution Context

The `ExecutionContext` class (defined in [execution_engine.py:55](execution_engine.py#L55)) maintains shared state:
- `work_directory`: Current project workspace
- `output_directory`: Final output location
- `project_variables`: Project metadata
- `cached_documentation`: Context7 docs cache
- `execution_results`: Task execution results

Access via `ExecutionEngine.context` after initialization.

## Output Files

Each execution generates:
- **Execution Report**: `<output_dir>/execution_report.json` (JSON format with plan, results, summary)
- **Project Documentation**: `<output_dir>/PROJECT_DOCUMENTATION.md` (Markdown summary)
- **Framework Log**: `framework.log` (in root directory)

## Testing a Single Component

```python
# Test TaskPlanner
from task_planner import TaskPlanner
planner = TaskPlanner()
plan = planner.create_execution_plan("Create a React app")
plan = planner.optimize_plan(plan)
print(f"Tasks: {len(plan.tasks)}")

# Test ExecutionEngine
import asyncio
from execution_engine import ExecutionEngine

config = {
    'framework': {'max_parallel_tasks': 5},
    'execution': {
        'work_directory': './workspace',
        'output_directory': './output'
    }
}
engine = ExecutionEngine(config)
results = asyncio.run(engine.execute_plan(plan))
```

## Common Development Tasks

### Modifying Task Generation Logic
Edit `TaskPlanner._generate_tasks()` in [task_planner.py:322](task_planner.py#L322).

### Changing Parallel Execution Strategy
Edit `TaskPlanner.optimize_plan()` in [task_planner.py:492](task_planner.py#L492).

### Adding Context7 Library Mappings
Edit `context7_mapping` dictionary in [task_planner.py:203](task_planner.py#L203).

### Customizing Execution Handlers
Edit task type handlers (e.g., `_execute_web_development`) in [execution_engine.py:327](execution_engine.py#L327).

### Modifying CLI Interface
Edit `main()` function in [main.py:249](main.py#L249).

## Debugging

Enable debug logging:
```bash
python orchestrator/main.py --log-level DEBUG --task "..."
```

Check execution report for detailed task results:
```bash
cat output/<project-name>/execution_report.json
```

Review framework log:
```bash
tail -f framework.log
```

## Project Structure Notes

- No nested `orchestrator/orchestrator/` structure—core modules are directly in root
- `main.py` is in root, imports from `task_planner` and `execution_engine` directly
- Configuration files expected in `./config/` or root (e.g., `./mcp-registry.yaml`)
- No `config/` directory currently exists—configs are in root
