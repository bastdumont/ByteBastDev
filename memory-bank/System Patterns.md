# System Patterns

## Naming Conventions

### File Naming

**Python Files:**
- Modules: `snake_case.py` (e.g., `task_planner.py`, `execution_engine.py`)
- Classes: `PascalCase` (e.g., `TaskPlanner`, `ExecutionEngine`)
- Functions/Methods: `snake_case` (e.g., `create_execution_plan()`, `execute_task()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_PARALLEL_TASKS`, `DEFAULT_TIMEOUT`)

**Configuration Files:**
- YAML configs: `kebab-case.yaml` (e.g., `framework-config.yaml`, `mcp-registry.yaml`)
- Template files: `kebab-case.yaml` or `PascalCase.tsx` depending on context

**Project Templates:**
- Directory names: `kebab-case` (e.g., `next-js-saas`, `react-dashboard`)
- Template metadata: `template.yaml`

### Class Naming

**Core Components:**
- `TaskPlanner` - Task decomposition and planning
- `ExecutionEngine` - Task orchestration and execution
- `ExecutionContext` - Shared execution state
- `Task`, `TaskRequirement`, `ExecutionPlan` - Data classes

**Handlers:**
- `*Handler` suffix for MCP handlers (e.g., `MongoDBHandler`, `StripeHandler`)
- `*Adapter` suffix for skill adapters (e.g., `WebSkillsAdapter`, `DocumentSkillsAdapter`)

**Utilities:**
- `FileManager` - File operations
- `CodeValidator`, `SecurityValidator` - Validation
- `PromptBuilder` - Prompt generation
- `ConfigLoader` - Configuration management
- `TemplateEngine` - Template rendering
- `Logger` - Logging system

### Method Naming

**Patterns:**
- `create_*` - Creation methods (e.g., `create_execution_plan()`)
- `execute_*` - Execution methods (e.g., `execute_task()`)
- `validate_*` - Validation methods (e.g., `validate_python_code()`)
- `get_*` - Retrieval methods (e.g., `get_documentation()`)
- `register_*` - Registration methods (e.g., `register_mcp_handlers()`)
- `_*` - Private methods (e.g., `_resolve_dependencies()`)

## Code Style & Architecture Patterns

### Python Style Guide

**Type Hints:**
```python
def create_task(
    name: str,
    description: str,
    task_type: TaskType,
    dependencies: List[str] = None
) -> Task:
    """Create a new task with type hints"""
    pass
```

**Docstrings:**
```python
def execute_task(self, task: Task) -> Dict[str, Any]:
    """
    Execute a single task
    
    Args:
        task: Task instance to execute
        
    Returns:
        Dictionary with execution results including:
        - success: bool
        - output: Any
        - error: Optional[str]
        - duration: float
    """
    pass
```

**Async Pattern:**
```python
async def execute_task(self, task: Task) -> Dict[str, Any]:
    """All handlers use async/await pattern"""
    result = await self._handler.execute(task)
    return result
```

### Design Patterns Used

1. **Strategy Pattern**
   - Task type handlers in `ExecutionEngine`
   - Different execution strategies per task type

2. **Factory Pattern**
   - Handler creation in `ExecutionEngine._register_mcp_handlers()`
   - Skill adapter instantiation

3. **Observer Pattern**
   - Logging system with multiple handlers
   - Progress tracking and callbacks

4. **Builder Pattern**
   - `PromptBuilder` for constructing prompts
   - `ExecutionPlan` construction in `TaskPlanner`

5. **Repository Pattern**
   - MCP handlers abstract external service access
   - Skill adapters abstract skill execution

6. **Dependency Injection**
   - Configuration passed to all classes
   - Handlers receive config on initialization

### Architecture Patterns

**Layered Architecture:**
```
CLI Layer (main.py)
    ↓
Orchestration Layer (task_planner, execution_engine)
    ↓
Integration Layer (mcp_handlers, skill_adapters)
    ↓
External Services (MCPs, Skills, Context7)
```

**Separation of Concerns:**
- **Planning**: `TaskPlanner` - Pure planning logic
- **Execution**: `ExecutionEngine` - Orchestration only
- **Integration**: Handlers/Adapters - Service-specific logic
- **Utilities**: Shared utilities (file, validation, logging)

**Configuration Management:**
- Three-level config system: Default → Global → Project
- Deep merge strategy for nested configs
- Environment variable substitution
- Dot notation access (`config.get('framework.max_parallel_tasks')`)

### Error Handling Patterns

**Return Format:**
```python
{
    'success': bool,
    'data': Any,
    'error': Optional[str],
    'metadata': Dict[str, Any]
}
```

**Retry Logic:**
- Configurable retries (default: 3)
- Exponential backoff
- Retryable vs non-retryable errors

**Exception Handling:**
- Specific exception types per handler
- Graceful degradation
- Detailed error logging
- User-friendly error messages

### Async/Await Patterns

**All I/O Operations:**
```python
async def fetch_documentation(self, library: str) -> Dict[str, Any]:
    """All external calls are async"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Parallel Execution:**
```python
results = await asyncio.gather(
    *[self.execute_task(task) for task in parallel_group]
)
```

### Validation Patterns

**Code Validation:**
- AST-based analysis for Python
- Regex patterns for common issues
- Security vulnerability scanning
- Best practices checking

**Input Validation:**
- Pydantic models for configuration
- Type checking with type hints
- Sanitization of user inputs
- File size and extension checks

## Styling Conventions

### Code Formatting

**Python:**
- Black formatting (configured in framework-config.yaml)
- Line length: 100 characters (default)
- Import sorting: Standard library → Third-party → Local

**JavaScript/TypeScript:**
- Prettier formatting (configured)
- ES2022+ syntax
- TypeScript strict mode

### Documentation Style

**Markdown Files:**
- Headers with clear hierarchy
- Code blocks with language tags
- Tables for structured data
- Examples in every major section

**Code Comments:**
- Docstrings for all public methods
- Inline comments for complex logic
- TODO comments for future work
- Type hints as documentation

### Project Structure

**Directory Organization:**
```
ByteClaude/
├── orchestrator/     # Core orchestration logic
├── integrations/     # External integrations
├── templates/       # Project templates and prompts
├── utils/           # Shared utilities
├── config/          # Configuration files
├── examples/        # Example projects
└── tests/           # Test suites
```

**File Organization:**
- One class per file (when reasonable)
- Related utilities grouped in modules
- Clear imports at top of file
- Consistent module structure

## Best Practices

### Code Quality

1. **Type Safety**: All functions have type hints
2. **Documentation**: All public APIs documented
3. **Error Handling**: Comprehensive error handling
4. **Testing**: Unit tests for critical paths (planned)
5. **Validation**: Input validation at boundaries

### Performance

1. **Parallel Execution**: Maximize parallel tasks
2. **Caching**: Context7 docs cached with TTL
3. **Lazy Loading**: Resources loaded on-demand
4. **Async I/O**: Non-blocking operations

### Security

1. **Input Validation**: All inputs validated
2. **Sanitization**: Output sanitized
3. **Secrets Management**: Environment variables only
4. **File Access**: Restricted paths for filesystem operations
5. **Dependency Scanning**: Security vulnerability checks

### Maintainability

1. **Modular Design**: Clear separation of concerns
2. **Configuration**: Externalized configuration
3. **Logging**: Comprehensive logging system
4. **Documentation**: Self-documenting code
5. **Extensibility**: Plugin-ready architecture

