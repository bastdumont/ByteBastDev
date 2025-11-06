# System Architecture

Complete technical overview of ByteClaude's architecture.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Natural Language Input                      │
│         "Create a React dashboard with MongoDB"             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK PLANNER                              │
│  • Parse request      • Detect technologies                 │
│  • Extract keywords   • Map to resources                    │
│  • Analyze goals      • Create execution plan               │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                 DEPENDENCY RESOLUTION                        │
│  • Build dependency graph    • Detect circular deps         │
│  • Topological sorting       • Identify parallel groups     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                 EXECUTION ENGINE                             │
│  • Orchestrate tasks    • Manage state    • Track progress  │
│  • Handle errors        • Execute retries                   │
└──┬─────────────────────┬─────────────────────┬──────────────┘
   │                     │                     │
   ▼                     ▼                     ▼
┌──────────────┐  ┌─────────────┐  ┌──────────────────┐
│  Context7    │  │   Skills    │  │   MCP Handlers   │
│  Client      │  │  • docx     │  │   • mongodb      │
│              │  │  • pdf      │  │   • stripe       │
│  • Resolve   │  │  • pptx     │  │   • notion       │
│  • Fetch     │  │  • artifacts│  │   • airtable     │
│  • Cache     │  │  • theme    │  │   • chrome       │
│              │  │  • canvas   │  │   • filesystem   │
└──────────────┘  └─────────────┘  └──────────────────┘
   │                     │                     │
   └─────────────────────┴─────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Monitoring &     │
              │ Validation       │
              └──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Output Files    │
              │  & Reports       │
              └──────────────────┘
```

## Core Components

### 1. Task Planner (`task_planner.py`)

**Purpose**: Analyze requirements and create execution plan

**Key Responsibilities**:
- Parse natural language requests
- Detect technologies and map to resources
- Decompose into structured tasks
- Resolve dependencies
- Optimize execution order
- Calculate estimates

**Key Methods**:
```python
analyze_request(request: str) -> Analysis
create_execution_plan(request: str) -> ExecutionPlan
optimize_plan(plan: ExecutionPlan) -> OptimizedPlan
```

**Example Flow**:
```
Input: "Create React app with MongoDB"
  ↓
Analysis: {technologies: [React, MongoDB], mcps: [mongodb], skills: [artifacts]}
  ↓
Tasks:
  1. Setup (CRITICAL, ~2s)
  2. Fetch Docs (HIGH, ~8s)
  3. Generate Code (CRITICAL, ~45s)
  4. Integrate (HIGH, ~12s)
  5. Test (MEDIUM, ~15s)
  6. Validate (MEDIUM, ~5s)
  ↓
Optimized Plan (parallel groups):
  Group 1: [Setup, Fetch Docs] → 8s
  Group 2: [Generate Code] → 45s
  Group 3: [Integrate, Test] → 20s (parallel)
  Group 4: [Validate] → 5s
  Total: ~78s
```

### 2. Execution Engine (`execution_engine.py`)

**Purpose**: Orchestrate task execution with state management

**Key Responsibilities**:
- Execute tasks sequentially or in parallel
- Manage execution context
- Handle errors with retries
- Save checkpoints for resumability
- Validate outputs
- Track progress

**Key Methods**:
```python
async execute_plan(plan: ExecutionPlan) -> ExecutionResults
execute_task(task: Task) -> TaskResult
_check_dependencies(task: Task) -> bool
_handle_error(error: Exception) -> RetryAction
```

**Execution Context**:
```python
@dataclass
class ExecutionContext:
    work_directory: str
    output_directory: str
    project_variables: Dict[str, Any]
    cached_documentation: Dict[str, str]
    execution_results: Dict[str, TaskResult]
```

### 3. Context7 Client (`context7_client.py`)

**Purpose**: Fetch and cache documentation

**Key Responsibilities**:
- Resolve library names to Context7 IDs
- Fetch documentation
- Manage cache
- Support multiple languages

**Example**:
```python
client = Context7Client()

# Resolve library
lib_id = client.resolve_library_id("react")
# Returns: "/facebook/react"

# Get docs
docs = client.get_library_docs("react", topic="hooks")
# Returns: Current React hooks documentation

# Cache automatic, TTL = 1 hour
```

### 4. MCP Handlers

**Purpose**: Handle external service integrations

**Included MCPs**:
| MCP | Purpose | Operations |
|-----|---------|-----------|
| MongoDB | NoSQL database | CRUD, aggregation, indexing |
| Stripe | Payment processing | Customers, products, invoices, subscriptions |
| Notion | Documentation | Pages, databases, blocks |
| Airtable | Cloud database | Records, tables, views |
| HubSpot | CRM | Contacts, companies, deals |
| Filesystem | File operations | Create, read, write, delete |
| Chrome | Browser automation | Navigation, clicks, screenshots |
| Web Tools | Web operations | Search, fetch, scrape |

**Handler Pattern**:
```python
class HandlerName:
    async def connect(self) -> bool
    async def operation(self, params) -> Result
    async def close(self) -> None
```

### 5. Skill Adapters

**Purpose**: Reusable task workflows

**Included Skills**:
| Skill | Purpose | Output |
|-------|---------|--------|
| docx | Word documents | .docx files |
| pdf | PDF documents | .pdf files |
| pptx | PowerPoint | .pptx files |
| xlsx | Excel spreadsheets | .xlsx files |
| artifacts-builder | React components | JSX/TSX |
| theme-factory | Design themes | CSS/JSON |
| canvas-design | Graphics | PNG/PDF |
| mcp-builder | MCP servers | Python/JS |
| skill-creator | New skills | Markdown |
| dev-tools | Development | Various |

## Data Flow

### Complete Execution Flow

```
1. INPUT PROCESSING
   └─ Parse natural language
   └─ Extract technologies
   └─ Identify constraints

2. ANALYSIS PHASE
   └─ Detect required MCPs
   └─ Identify required Skills
   └─ Map to Context7 libraries

3. PLANNING PHASE
   └─ Create task graph
   └─ Resolve dependencies
   └─ Optimize execution
   └─ Calculate estimates

4. PREPARATION PHASE
   └─ Create workspace
   └─ Initialize context
   └─ Fetch documentation
   └─ Verify MCP availability

5. EXECUTION PHASE
   └─ Execute tasks (sequential/parallel)
   └─ Manage state
   └─ Handle errors
   └─ Save checkpoints
   └─ Track progress

6. VALIDATION PHASE
   └─ Run tests
   └─ Check code quality
   └─ Validate output

7. DELIVERY PHASE
   └─ Generate documentation
   └─ Create reports
   └─ Archive outputs
```

## State Management

### ExecutionContext

Maintains shared state during execution:

```python
context = ExecutionContext(
    work_directory="./workspace/project_name",
    output_directory="./output/project_name",
    project_variables={
        "project_name": "my-app",
        "description": "My application",
        "created_at": 1730577845.23
    },
    cached_documentation={
        "react": {"content": "...", "fetched_at": "..."},
        "mongodb": {"content": "...", "fetched_at": "..."}
    },
    execution_results={
        "task_1": TaskResult(...),
        "task_2": TaskResult(...)
    }
)
```

## Parallel Execution

### Optimization Strategy

```
Sequential execution:
Task A → Task B → Task C → Task D
Duration: 30s + 45s + 60s + 25s = 160s

Dependency analysis:
A (no deps)
B (depends on A)
C (depends on A, B)
D (depends on B)

Parallel groups:
Group 1: [A] → 30s
Group 2: [B] → 45s (after A)
Group 3: [C, D] → 60s (parallel)
Total: 30 + 45 + 60 = 135s (16% faster!)

With more parallelism:
Group 1: [A, E, F] → 60s (max)
Group 2: [B, G] → 45s
Group 3: [C, D] → 60s
Total: 165s but faster perceived time
```

## Error Handling

### Retry Strategy

```
attempt = 0
max_retries = 3
retry_delay = 5  # seconds

while attempt < max_retries:
    try:
        result = execute_task(task)
        break
    except RetryableError as e:
        attempt += 1
        if attempt < max_retries:
            wait(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            handle_critical_failure(e)
```

### Critical vs Non-Critical Failures

**Critical (STOP)**:
- Project setup failure
- Required MCP unavailable
- Syntax errors in generated code

**Non-Critical (CONTINUE)**:
- Optional test failure
- Documentation generation issues
- Optional MCP failure

## Configuration System

### Three-Level Configuration

```
Layer 3: CLI Arguments (Highest Priority)
├─ --task "..."
├─ --output-dir ./custom
├─ --include-tests
└─ --log-level DEBUG
        │ (overrides)
        ▼
Layer 2: User Config
├─ config/framework-config.yaml
└─ .env file
        │ (overrides)
        ▼
Layer 1: Default Config (Lowest Priority)
└─ Built-in defaults

Final = Layer 1 + Layer 2 + Layer 3
```

## Technology Detection

### Technology → Resource Mapping

```python
tech_mcp_mapping = {
    'stripe': 'stripe',
    'mongodb': 'mongodb',
    'notion': 'notion',
    'airtable': 'airtable',
    'hubspot': 'hubspot'
}

tech_skill_mapping = {
    'react': 'artifacts-builder',
    'pdf': 'pdf',
    'word': 'docx',
    'excel': 'xlsx'
}

context7_mapping = {
    'react': '/facebook/react',
    'next.js': '/vercel/next.js',
    'mongodb': '/mongodb/docs',
    'stripe': '/stripe/stripe-node'
}
```

## Performance Metrics

### Typical Execution Times

| Task | Duration | Factor |
|------|----------|--------|
| Project setup | 1-2s | Filesystem |
| Fetch docs | 3-8s | Network |
| Code generation | 30-60s | AI inference |
| Integration | 5-15s | Template merge |
| Testing | 10-20s | Test framework |
| Validation | 2-5s | Checks |

### Optimization Techniques

1. **Parallel Execution**: Up to 5 concurrent tasks
2. **Caching**: Context7 docs cached for 1 hour
3. **Lazy Loading**: Resources loaded on-demand
4. **Early Exit**: Stop on critical failure
5. **Resource Pooling**: Reuse connections

## Security Considerations

- **Input Validation**: All inputs sanitized
- **File Operations**: Restricted to workspace
- **MCP Isolation**: Each MCP runs independently
- **API Keys**: Stored in environment variables
- **Output Review**: Generated code reviewed

## Next Steps

- [Task Planning Details](task-planning.md)
- [Execution Engine Details](execution-engine.md)
- [Integration Guide](../features/integration/overview.md)
- [API Reference](../api/task-planner.md)

