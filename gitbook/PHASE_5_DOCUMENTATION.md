# Phase 5: Advanced Features - Complete Documentation

**Phase**: 5/7 (71% Complete)
**Status**: ✅ COMPLETE
**Release Date**: December 2024
**Lines of Code**: ~1,430
**Files Created**: 5
**Components**: 5 Advanced Features

---

## Table of Contents

1. [Overview](#overview)
2. [Component Details](#component-details)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Usage Guides](#usage-guides)
6. [API Reference](#api-reference)
7. [Code Examples](#code-examples)
8. [Integration Patterns](#integration-patterns)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

Phase 5 delivers advanced features that enhance ByteClaude with sophisticated workflow management, beautiful user interfaces, extensibility mechanisms, and real-time monitoring capabilities.

### Phase Goals Achieved

✅ **Workflow Management**: Visual and programmatic workflow creation  
✅ **User Experience**: Beautiful CLI and web interfaces  
✅ **Extensibility**: Plugin system for custom extensions  
✅ **Monitoring**: Real-time execution tracking and metrics  
✅ **Integration**: REST API for external system integration  

### Key Features

- **Workflow Designer**: Create and manage workflows visually or programmatically
- **Enhanced CLI**: Beautiful terminal interface with interactive features
- **Plugin System**: Extensible architecture for custom plugins
- **Web UI**: Beautiful dashboard with workflow management
- **Monitoring Dashboard**: Real-time execution metrics and analytics

---

## Component Details

### 1. Workflow Designer

**File**: `orchestrator/workflow_designer.py`  
**Lines**: ~280  
**Classes**: 4  
**Purpose**: Programmatic workflow creation and visual management

#### Key Classes

```python
class NodeType(Enum):
    """Types of workflow nodes"""
    TASK = "task"
    DECISION = "decision"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    START = "start"
    END = "end"

class WorkflowNode:
    """Represents a node in the workflow"""
    - id: str
    - type: NodeType
    - title: str
    - description: str
    - config: Dict[str, Any]
    - inputs: List[str]
    - outputs: List[str]
    - dependencies: List[str]

class WorkflowConnection:
    """Represents a connection between nodes"""
    - source_id: str
    - target_id: str
    - label: str
    - condition: str

class WorkflowDesigner:
    """Main workflow designer class"""
    - add_node(node_id, type, title, description, config)
    - connect_nodes(source_id, target_id, label, condition)
    - get_execution_order() -> List[str]
    - to_yaml() -> str
    - to_json() -> str
    - from_dict(data) -> WorkflowDesigner
    - generate_diagram() -> str
    - validate() -> (bool, List[str])

class WorkflowBuilder:
    """Fluent interface for building workflows"""
    - start(title) -> WorkflowBuilder
    - task(task_id, title, description, config) -> WorkflowBuilder
    - connect(source_id, target_id, label) -> WorkflowBuilder
    - end(title) -> WorkflowBuilder
    - build() -> WorkflowDesigner
```

#### Features

- **Node Management**: Create and manage workflow nodes
- **Connection Management**: Define dependencies between nodes
- **Execution Order**: Topological sorting for optimal execution
- **Validation**: Cycle detection and orphan node checking
- **Serialization**: YAML/JSON export/import
- **Visualization**: ASCII diagram generation
- **Fluent API**: Builder pattern for easy workflow creation

#### Supported Node Types

- **TASK**: Regular task node
- **DECISION**: Conditional branching
- **PARALLEL**: Parallel execution group
- **SEQUENTIAL**: Sequential execution group
- **START**: Workflow entry point
- **END**: Workflow exit point

---

### 2. Enhanced CLI

**File**: `orchestrator/cli_enhanced.py`  
**Lines**: ~280  
**Classes**: 2  
**Purpose**: Beautiful terminal interface with rich formatting

#### Key Classes

```python
class UILevel(Enum):
    """Output verbosity levels"""
    MINIMAL = "minimal"      # Minimal output
    NORMAL = "normal"        # Standard output
    VERBOSE = "verbose"      # Detailed output

class EnhancedCLI:
    """Main CLI class with rich formatting"""
    - __init__(level: UILevel)
    - print_welcome()
    - print_section(title, content)
    - print_table(data, headers, title)
    - print_code(code, language, title)
    - print_error(message)
    - print_success(message)
    - print_warning(message)
    - print_info(message)
    - prompt_input(prompt, default) -> str
    - prompt_confirm(prompt, default) -> bool
    - show_progress(description, total) -> ProgressBar
    - print_workflow(workflow_data)
    - interactive_menu(title, options, prompt) -> int
    - save_command(command)
    - show_help(command_help)
```

#### Features

- **Rich Integration**: Beautiful formatting with Rich library
- **Graceful Fallback**: Works without Rich library
- **Interactive Prompts**: User input with validation
- **Progress Tracking**: Visual progress bars
- **Multiple Formats**: Tables, panels, trees, code highlighting
- **Status Messages**: Color-coded success/error/warning/info
- **Command History**: Track user commands
- **Verbosity Levels**: Control output detail

#### Output Formats

- **Tables**: Formatted data tables
- **Panels**: Boxed content sections
- **Trees**: Hierarchical data display
- **Code**: Syntax-highlighted code blocks
- **Progress**: Visual progress indicators
- **Menus**: Interactive option selection

---

### 3. Plugin System

**File**: `orchestrator/plugin_system.py`  
**Lines**: ~270  
**Classes**: 4  
**Purpose**: Extensible architecture for custom plugins

#### Key Classes

```python
class PluginMetadata:
    """Plugin metadata"""
    - name: str
    - version: str
    - author: str
    - description: str
    - entry_point: str
    - dependencies: List[str]
    - hooks: Dict[str, List[str]]

class Hook(ABC):
    """Base class for hooks"""
    - execute(*args, **kwargs) -> Any

class Plugin(ABC):
    """Base class for all plugins"""
    @property
    - metadata: PluginMetadata
    - initialize(context: Dict[str, Any])
    - execute(*args, **kwargs) -> Any

class PluginManager:
    """Manages plugin loading and execution"""
    - register_hook(hook_name, hook)
    - execute_hooks(hook_name, *args, **kwargs) -> List[Any]
    - load_plugin(plugin_path) -> Plugin
    - load_plugins_from_directory(directory) -> List[Plugin]
    - execute_plugin(plugin_name, *args, **kwargs) -> Any
    - get_plugin(plugin_name) -> Plugin
    - list_plugins() -> List[PluginMetadata]
    - unload_plugin(plugin_name) -> bool

class PluginRegistry:
    """Global plugin registry (Singleton)"""
    - register(metadata)
    - unregister(plugin_name)
    - get(plugin_name) -> PluginMetadata
    - list_all() -> List[PluginMetadata]
    - search(query) -> List[PluginMetadata]
```

#### Features

- **Extensible Architecture**: Easy plugin development
- **Hook System**: Event-based plugin execution
- **Dynamic Loading**: Load plugins at runtime
- **Plugin Registry**: Discover available plugins
- **Metadata Support**: Plugin information tracking
- **Dependency Management**: Track plugin dependencies
- **Context Support**: Pass context to plugins

#### Hook Types

- **pre_execution**: Before task execution
- **post_execution**: After task execution
- **on_error**: On execution error
- **on_warning**: On warning
- **on_complete**: On completion

---

### 4. Web UI Interface

**File**: `orchestrator/web_ui.py`  
**Lines**: ~320  
**Classes**: 1  
**Purpose**: Browser-based workflow management interface

#### Key Class

```python
class WebUIServer:
    """Flask-based web UI server"""
    - __init__(host, port, debug)
    - _setup_routes()
    - _get_html_content() -> str
    - run()
```

#### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main dashboard |
| GET | `/api/health` | Health check |
| GET | `/api/workflows` | List all workflows |
| POST | `/api/workflows` | Create workflow |
| GET | `/api/workflows/<id>` | Get workflow details |
| POST | `/api/workflows/<id>/execute` | Execute workflow |
| GET | `/api/executions` | List executions |
| GET | `/api/executions/<id>` | Get execution details |

#### Features

- **Beautiful Dashboard**: Responsive gradient design
- **Workflow Management**: Create and view workflows
- **Execution Tracking**: Monitor execution status
- **Real-time Updates**: JavaScript-based updates
- **System Status**: Health monitoring
- **Quick Actions**: Easy workflow operations
- **REST API**: External integration support

#### Request/Response Examples

```python
# Create Workflow
POST /api/workflows
{
    "name": "Data Pipeline",
    "description": "ETL workflow",
    "nodes": [],
    "connections": []
}

Response (201):
{
    "id": "workflow_1",
    "name": "Data Pipeline",
    "status": "draft",
    "created_at": "2024-12-01T10:00:00",
    ...
}

# Execute Workflow
POST /api/workflows/workflow_1/execute

Response (202):
{
    "id": "exec_1",
    "workflow_id": "workflow_1",
    "status": "running",
    "started_at": "2024-12-01T10:05:00",
    "progress": 0
}

# Get Health Status
GET /api/health

Response (200):
{
    "status": "healthy",
    "timestamp": "2024-12-01T10:06:00",
    "workflows_count": 5,
    "executions_count": 3
}
```

---

### 5. Monitoring Dashboard

**File**: `orchestrator/monitoring_dashboard.py`  
**Lines**: ~280  
**Classes**: 3  
**Purpose**: Real-time execution metrics and performance tracking

#### Key Classes

```python
class ExecutionStatus(Enum):
    """Execution status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskMetrics:
    """Metrics for a single task"""
    - task_id: str
    - name: str
    - status: ExecutionStatus
    - start_time: datetime
    - end_time: datetime
    - errors: List[str]
    - warnings: List[str]
    - elapsed_time: float (property)

class ExecutionMetrics:
    """Metrics for complete execution"""
    - execution_id: str
    - workflow_name: str
    - status: ExecutionStatus
    - tasks: List[TaskMetrics]
    - total_tasks: int
    - completed_tasks: int
    - failed_tasks: int
    - total_errors: int
    - total_warnings: int
    - progress_percentage: float (property)
    - success_rate: float (property)
    - total_duration: float (property)

class MonitoringDashboard:
    """Main monitoring dashboard"""
    - create_execution(execution_id, workflow_name, total_tasks)
    - start_task(execution_id, task_id, task_name) -> TaskMetrics
    - complete_task(execution_id, task_id, success, errors, warnings)
    - complete_execution(execution_id)
    - get_execution_metrics(execution_id) -> ExecutionMetrics
    - get_all_executions() -> List[ExecutionMetrics]
    - get_current_execution() -> ExecutionMetrics
    - get_summary() -> Dict[str, Any]
    - get_performance_stats() -> Dict[str, Any]
    - export_report(execution_id) -> Dict[str, Any]
```

#### Features

- **Real-time Metrics**: Track execution progress
- **Task Tracking**: Monitor individual task performance
- **Performance Analytics**: Execution time analysis
- **Success Metrics**: Calculate success rates
- **Error Tracking**: Aggregate errors and warnings
- **Report Export**: Generate detailed reports
- **Performance Stats**: Average, min, max metrics

#### Metrics Tracked

- Execution duration
- Task completion status
- Error/warning counts
- Success rates
- Progress percentage
- Performance statistics
- Task performance

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
└──────────┬───────────────────────────────┬──────────────────┘
           │                               │
    ┌──────▼──────┐              ┌────────▼────────┐
    │   Web UI    │              │  CLI Interface  │
    │  (Browser)  │              │  (Terminal)     │
    └──────┬──────┘              └────────┬────────┘
           │                               │
    ┌──────▼──────────────────────────────▼────────┐
    │           Web UI Server (Flask)              │
    │  - REST API Endpoints                        │
    │  - Dashboard HTML/CSS/JS                     │
    │  - Real-time Updates                         │
    └──────┬─────────────────────────────────┬────┘
           │                                 │
    ┌──────▼──────────────┐    ┌────────────▼──────┐
    │ Workflow Designer   │    │ Plugin System     │
    │ - Visual Workflows  │    │ - Custom Plugins  │
    │ - Topological Sort  │    │ - Hook Events     │
    │ - Validation        │    │ - Dynamic Load    │
    └──────┬──────────────┘    └────────────┬──────┘
           │                                │
    ┌──────▼──────────────────────────────▼─────────┐
    │      Monitoring Dashboard                      │
    │ - Real-time Metrics                           │
    │ - Performance Tracking                        │
    │ - Report Generation                           │
    └──────────────────────────────────────────────┘
```

### Component Interactions

```
Workflow Designer
    ↓
Creates execution plan with nodes & connections
    ↓
Plugin System
    ↓
Executes pre-execution hooks
    ↓
Monitoring Dashboard
    ↓
Tracks task start/completion
    ↓
Plugin System
    ↓
Executes post-execution hooks
    ↓
Generate reports & metrics
```

---

## Installation & Setup

### Prerequisites

```bash
# Python 3.8+
python --version

# Required packages
pip install flask flask-cors pyyaml

# Optional (for Rich CLI)
pip install rich
```

### Installation Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/bastdumont/BalderFrameWork.git
   cd BalderFrameWork
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start web server**
   ```bash
   python orchestrator/main.py
   ```

4. **Access web UI**
   ```
   http://localhost:5000
   ```

### Configuration

**Environment Variables**
```bash
BYTECLAUDE_HOST=localhost
BYTECLAUDE_PORT=5000
BYTECLAUDE_DEBUG=false
BYTECLAUDE_LOG_LEVEL=INFO
```

**Configuration File** (`config/framework-config.yaml`)
```yaml
web_ui:
  host: localhost
  port: 5000
  debug: false

cli:
  ui_level: normal
  colors: true

plugins:
  auto_load_directory: ./plugins
  enable_hooks: true

monitoring:
  track_metrics: true
  export_reports: true
```

---

## Usage Guides

### Quick Start

#### 1. Create a Workflow

```python
from orchestrator.workflow_designer import WorkflowBuilder

# Create workflow
builder = WorkflowBuilder()
workflow = (builder
    .start("Begin")
    .task("analyze", "Analyze Requirements", "Understand project")
    .task("plan", "Create Plan", "Decompose into tasks")
    .task("implement", "Implement Solution", "Write code")
    .task("test", "Test Solution", "Quality assurance")
    .task("deploy", "Deploy", "Production release")
    .end("Complete")
    .connect("start", "analyze")
    .connect("analyze", "plan")
    .connect("plan", "implement")
    .connect("implement", "test")
    .connect("test", "deploy")
    .connect("deploy", "end")
    .build())

# Validate workflow
is_valid, errors = workflow.validate()
if not is_valid:
    print(f"Validation errors: {errors}")

# Get execution order
order = workflow.get_execution_order()
print(f"Execution order: {order}")

# Generate diagram
print(workflow.generate_diagram())

# Export to YAML
yaml_content = workflow.to_yaml()
```

#### 2. Use Enhanced CLI

```python
from orchestrator.cli_enhanced import create_cli, UILevel

# Create CLI instance
cli = create_cli(UILevel.NORMAL)

# Print welcome
cli.print_welcome()

# Print sections
cli.print_section("Getting Started", "Welcome to ByteClaude!")

# Print tables
cli.print_table(
    [["Task", "Status"], ["Analyze", "Complete"], ["Plan", "In Progress"]],
    ["Task Name", "Status"],
    "Project Progress"
)

# Print code
cli.print_code("def hello(): print('Hello')", "python", "Example Code")

# Interactive prompts
name = cli.prompt_input("Enter your name", "User")
confirm = cli.prompt_confirm("Continue?", True)

# Status messages
cli.print_success("Operation completed!")
cli.print_error("An error occurred!")
cli.print_warning("Warning message")
cli.print_info("Information message")

# Interactive menu
choice = cli.interactive_menu(
    "Select an option",
    ["Create Workflow", "View Workflows", "Monitor Execution"],
    "Your choice"
)
```

#### 3. Create Plugins

```python
from orchestrator.plugin_system import Plugin, PluginMetadata, PluginManager

# Define custom plugin
class DataValidationPlugin(Plugin):
    @property
    def metadata(self):
        return PluginMetadata(
            name="data-validator",
            version="1.0.0",
            author="Developer",
            description="Validates data during execution",
            entry_point="DataValidationPlugin",
            dependencies=[]
        )
    
    def initialize(self, context):
        self.context = context
        print(f"Initialized {self.metadata.name}")
    
    def execute(self, data):
        # Validate data
        if not data:
            return {"valid": False, "message": "Empty data"}
        
        return {
            "valid": True,
            "record_count": len(data),
            "message": "Data valid"
        }

# Use plugin
manager = PluginManager()
manager.load_plugin("data_validator.py")
result = manager.execute_plugin("data-validator", my_data)
```

#### 4. Monitor Execution

```python
from orchestrator.monitoring_dashboard import create_dashboard

# Create dashboard
dashboard = create_dashboard()

# Create execution
execution = dashboard.create_execution(
    "exec_001",
    "My Workflow",
    total_tasks=5
)

# Track tasks
for i in range(5):
    # Start task
    task = dashboard.start_task("exec_001", f"task_{i}", f"Task {i}")
    
    # Simulate work
    import time
    time.sleep(1)
    
    # Complete task
    dashboard.complete_task(
        "exec_001",
        f"task_{i}",
        success=True,
        warnings=[] if i % 2 == 0 else ["Minor issue"]
    )

# Complete execution
dashboard.complete_execution("exec_001")

# Get metrics
metrics = dashboard.get_execution_metrics("exec_001")
print(f"Success rate: {metrics.success_rate}%")
print(f"Total duration: {metrics.total_duration}s")

# Export report
report = dashboard.export_report("exec_001")
```

---

## API Reference

### Workflow Designer API

#### `WorkflowDesigner.add_node()`
```python
def add_node(
    node_id: str,
    node_type: NodeType,
    title: str,
    description: str = "",
    config: Dict[str, Any] = None
) -> WorkflowNode
```

#### `WorkflowDesigner.get_execution_order()`
```python
def get_execution_order() -> List[str]:
    """Return topologically sorted node IDs"""
```

#### `WorkflowDesigner.validate()`
```python
def validate() -> tuple[bool, List[str]]:
    """Validate workflow structure, return (is_valid, errors)"""
```

---

### Enhanced CLI API

#### `EnhancedCLI.print_table()`
```python
def print_table(
    data: List[List[Any]],
    headers: List[str],
    title: str = ""
) -> None
```

#### `EnhancedCLI.prompt_input()`
```python
def prompt_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default"""
```

#### `EnhancedCLI.interactive_menu()`
```python
def interactive_menu(
    title: str,
    options: List[str],
    prompt: str = "Choose an option"
) -> int:
    """Show menu and return selected index"""
```

---

### Plugin System API

#### `PluginManager.load_plugin()`
```python
def load_plugin(plugin_path: str) -> Plugin:
    """Load plugin from file path"""
```

#### `PluginManager.execute_plugin()`
```python
def execute_plugin(plugin_name: str, *args, **kwargs) -> Any:
    """Execute named plugin"""
```

---

### Web UI API

#### Health Check
```
GET /api/health
Returns: {status, timestamp, workflows_count, executions_count}
```

#### Create Workflow
```
POST /api/workflows
Body: {name, description, nodes, connections}
Returns: {id, name, status, created_at, ...}
```

#### Execute Workflow
```
POST /api/workflows/{workflow_id}/execute
Returns: {id, workflow_id, status, started_at, progress}
```

---

### Monitoring Dashboard API

#### `MonitoringDashboard.create_execution()`
```python
def create_execution(
    execution_id: str,
    workflow_name: str,
    total_tasks: int
) -> ExecutionMetrics
```

#### `MonitoringDashboard.complete_task()`
```python
def complete_task(
    execution_id: str,
    task_id: str,
    success: bool = True,
    errors: List[str] = None,
    warnings: List[str] = None
) -> None
```

#### `MonitoringDashboard.export_report()`
```python
def export_report(execution_id: str) -> Dict[str, Any]:
    """Export detailed execution report"""
```

---

## Code Examples

### Example 1: Complete Workflow Execution

```python
from orchestrator.workflow_designer import WorkflowBuilder
from orchestrator.monitoring_dashboard import create_dashboard
from orchestrator.cli_enhanced import create_cli, UILevel

# Create CLI
cli = create_cli(UILevel.NORMAL)
cli.print_welcome()

# Create workflow
workflow = (WorkflowBuilder()
    .start()
    .task("t1", "Validate Data")
    .task("t2", "Process Data")
    .task("t3", "Generate Report")
    .end()
    .connect("start", "t1")
    .connect("t1", "t2")
    .connect("t2", "t3")
    .connect("t3", "end")
    .build())

# Validate
if not workflow.validate()[0]:
    cli.print_error("Invalid workflow")
    exit(1)

cli.print_success("Workflow validated")

# Create dashboard
dashboard = create_dashboard()
execution = dashboard.create_execution("exec_1", "Data Pipeline", 3)

# Execute tasks
for task_id in workflow.get_execution_order()[1:-1]:  # Skip start/end
    dashboard.start_task("exec_1", task_id, f"Executing {task_id}")
    
    # Simulate work
    import time
    time.sleep(1)
    
    dashboard.complete_task("exec_1", task_id, success=True)

dashboard.complete_execution("exec_1")

# Show results
report = dashboard.export_report("exec_1")
cli.print_section("Execution Report", f"""
Success Rate: {report['execution']['success_rate']:.1f}%
Duration: {report['execution']['duration']:.2f}s
Tasks Completed: {report['execution']['summary']['completed_tasks']}
""")
```

### Example 2: Plugin Development

```python
# my_custom_plugin.py
from orchestrator.plugin_system import Plugin, PluginMetadata

class MetricsCollectorPlugin(Plugin):
    """Collects custom metrics during execution"""
    
    @property
    def metadata(self):
        return PluginMetadata(
            name="metrics-collector",
            version="1.0.0",
            author="My Team",
            description="Collects performance metrics",
            entry_point="MetricsCollectorPlugin"
        )
    
    def initialize(self, context):
        self.metrics = {}
        self.context = context
    
    def execute(self, task_id, metrics_data):
        # Collect metrics
        self.metrics[task_id] = {
            "duration": metrics_data.get("duration", 0),
            "memory_used": metrics_data.get("memory", 0),
            "timestamp": metrics_data.get("timestamp")
        }
        
        return {
            "status": "collected",
            "metric_count": len(self.metrics)
        }
    
    def get_summary(self):
        total_duration = sum(m["duration"] for m in self.metrics.values())
        return {
            "total_tasks": len(self.metrics),
            "total_duration": total_duration,
            "avg_duration": total_duration / len(self.metrics) if self.metrics else 0
        }

# Use the plugin
from orchestrator.plugin_system import PluginManager

manager = PluginManager()
plugin = manager.load_plugin("my_custom_plugin.py")

# Execute plugin
result = manager.execute_plugin("metrics-collector", "task_1", {
    "duration": 2.5,
    "memory": 256,
    "timestamp": "2024-12-01T10:00:00"
})

print(f"Collection result: {result}")
```

---

## Integration Patterns

### Pattern 1: CLI + Workflow Designer

```python
from orchestrator.cli_enhanced import create_cli
from orchestrator.workflow_designer import WorkflowBuilder

cli = create_cli()

# Get workflow details from user
name = cli.prompt_input("Workflow name")
task_count = int(cli.prompt_input("Number of tasks", "3"))

# Build workflow
builder = WorkflowBuilder().start()
for i in range(task_count):
    builder.task(f"task_{i}", f"Task {i}")

workflow = builder.end().build()

# Show workflow
cli.print_workflow(workflow.to_dict())
```

### Pattern 2: Web UI + Monitoring

```python
from orchestrator.web_ui import create_web_ui
from orchestrator.monitoring_dashboard import create_dashboard

# Create web UI
web_ui = create_web_ui("localhost", 5000)

# Share dashboard instance
dashboard = create_dashboard()
web_ui.dashboard = dashboard

# Run web server
web_ui.run()  # Now web UI can display metrics from dashboard
```

### Pattern 3: Plugins + Monitoring

```python
from orchestrator.plugin_system import PluginManager
from orchestrator.monitoring_dashboard import create_dashboard

manager = PluginManager()
dashboard = create_dashboard()

# Load plugins
manager.load_plugin("metrics_plugin.py")

# During execution
execution = dashboard.create_execution("exec_1", "Pipeline", 5)

for i in range(5):
    task = dashboard.start_task("exec_1", f"task_{i}", f"Task {i}")
    
    # Execute plugins
    result = manager.execute_plugin("metrics-collector", f"task_{i}", {
        "duration": 2.0,
        "memory": 512
    })
    
    dashboard.complete_task("exec_1", f"task_{i}", success=True)
```

---

## Best Practices

### Workflow Design

1. **Use Meaningful Node IDs**: Make IDs descriptive
   ```python
   # Good
   .task("validate_data", "Validate Input Data")
   
   # Avoid
   .task("t1", "Task")
   ```

2. **Document Workflow**: Add descriptions
   ```python
   .task("parse", "Parse Configuration", "Load and parse config files")
   ```

3. **Validate Before Execution**
   ```python
   is_valid, errors = workflow.validate()
   if errors:
       for error in errors:
           log_error(error)
   ```

4. **Use Fluent API**: Chain operations
   ```python
   workflow = (builder
       .start()
       .task("a", "A")
       .task("b", "B")
       .connect("start", "a")
       .connect("a", "b")
       .end()
       .build())
   ```

### Plugin Development

1. **Implement All Abstract Methods**
   ```python
   class MyPlugin(Plugin):
       @property
       def metadata(self):
           # Required
       
       def initialize(self, context):
           # Required
       
       def execute(self, *args, **kwargs):
           # Required
   ```

2. **Handle Errors Gracefully**
   ```python
   def execute(self, data):
       try:
           # Process data
           return {"status": "success"}
       except Exception as e:
           return {"status": "error", "message": str(e)}
   ```

3. **Document Plugin Metadata**
   ```python
   PluginMetadata(
       name="my-plugin",
       version="1.0.0",
       author="Team",
       description="What it does",
       entry_point="ClassName",
       dependencies=["package>=1.0.0"]
   )
   ```

### Monitoring

1. **Track Metrics Consistently**
   ```python
   dashboard.start_task(exec_id, task_id, task_name)
   # ... work ...
   dashboard.complete_task(exec_id, task_id, success=True)
   ```

2. **Use Proper Error Reporting**
   ```python
   dashboard.complete_task(
       execution_id,
       task_id,
       success=False,
       errors=["Connection timeout", "Retry failed"]
   )
   ```

3. **Generate Reports**
   ```python
   report = dashboard.export_report(execution_id)
   save_report_to_file(report)
   ```

---

## Troubleshooting

### Issue: Workflow Validation Fails

**Problem**: `workflow.validate()` returns errors

**Solutions**:
1. Check for orphaned nodes
   ```python
   is_valid, errors = workflow.validate()
   for error in errors:
       print(error)  # "Node 'X' is not connected"
   ```

2. Ensure all nodes are connected
   ```python
   # Make sure to connect all nodes
   .connect("start", "first_task")
   .connect("first_task", "next_task")
   .connect("last_task", "end")
   ```

3. Check for cycles
   ```python
   # Avoid circular dependencies
   # Don't do: A -> B -> A
   ```

### Issue: Plugin Not Loading

**Problem**: `PluginManager.load_plugin()` returns None

**Solutions**:
1. Verify file path
   ```python
   import os
   assert os.path.exists("my_plugin.py")
   ```

2. Check plugin class inheritance
   ```python
   class MyPlugin(Plugin):  # Must inherit from Plugin
       pass
   ```

3. Check metadata property
   ```python
   @property
   def metadata(self):  # Must be a property
       return PluginMetadata(...)
   ```

### Issue: Web UI Not Starting

**Problem**: Flask server won't start

**Solutions**:
1. Check port availability
   ```bash
   lsof -i :5000  # Check if port is in use
   ```

2. Install Flask
   ```bash
   pip install flask flask-cors
   ```

3. Check firewall
   ```bash
   # Allow port 5000
   ```

### Issue: Monitoring Metrics Not Tracking

**Problem**: Dashboard shows no data

**Solutions**:
1. Create execution first
   ```python
   execution = dashboard.create_execution("id", "name", 5)
   ```

2. Start and complete tasks
   ```python
   dashboard.start_task(exec_id, task_id, task_name)
   dashboard.complete_task(exec_id, task_id, success=True)
   ```

3. Check execution exists
   ```python
   metrics = dashboard.get_execution_metrics(exec_id)
   assert metrics is not None
   ```

---

## Summary

Phase 5 provides a complete advanced feature set for ByteClaude:

- **Workflow Designer**: Visual and programmatic workflow creation
- **Enhanced CLI**: Beautiful terminal interface
- **Plugin System**: Extensible architecture
- **Web UI**: Browser-based management
- **Monitoring Dashboard**: Real-time metrics

These components work together to provide a professional, extensible development automation framework.

---

**Document Version**: 1.0.0
**Last Updated**: December 2024
**Phase Status**: ✅ Complete (5/7)
**Next Phase**: Phase 6 - Data & Analytics
