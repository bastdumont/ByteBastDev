# Getting Started with ByteClaude Development

Welcome to ByteClaude - an AI-powered automated development framework. This guide will help you get started with using and extending the framework.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Architecture](#understanding-the-architecture)
3. [Using the Utilities](#using-the-utilities)
4. [Creating Boilerplates](#creating-boilerplates)
5. [Writing Expert Prompts](#writing-expert-prompts)
6. [Building MCP Handlers](#building-mcp-handlers)
7. [Contributing](#contributing)

---

## Quick Start

### Installation

```bash
# Clone the repository
cd ByteClaude

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py
```

### First Run

```bash
# Interactive mode
python orchestrator/main.py

# Single task
python orchestrator/main.py --task "Create a React app"

# Dry run (see plan without executing)
python orchestrator/main.py --task "Build a dashboard" --dry-run
```

---

## Understanding the Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│         Natural Language Input          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           Task Planner                  │
│   (Analyzes, decomposes, optimizes)    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Execution Engine                │
│   (Orchestrates Skills & MCPs)          │
└─────────┬──────────────┬────────────────┘
          │              │
          ▼              ▼
    ┌─────────┐    ┌──────────┐
    │ Skills  │    │   MCPs   │
    └─────────┘    └──────────┘
```

### Directory Structure

- **`orchestrator/`** - Core task planning and execution
- **`config/`** - Configuration files
- **`utils/`** - Utility modules (file ops, logging, validation, etc.)
- **`integrations/`** - External service integrations
- **`templates/`** - Project templates, workflows, prompts
- **`examples/`** - Example projects and tutorials

---

## Using the Utilities

### FileManager

```python
from utils import FileManager

# Create file manager
fm = FileManager(base_path="./my-project")

# Create directory structure
fm.create_directory_structure({
    'src': {
        'components': None,
        'utils': None
    },
    'tests': None
})

# Create files
fm.create_file("src/app.py", "print('Hello World')")

# Read/write JSON
data = fm.read_json("config.json")
fm.write_json("output.json", {'status': 'success'})

# Search files
python_files = fm.find_files(".", extensions=['.py'])
```

### Logger

```python
from utils import setup_logger, get_logger, LoggerContext

# Setup main logger
logger = setup_logger(
    name="my_app",
    level="DEBUG",
    log_file="app.log",
    use_colors=True
)

# Use logger
logger.info("Application started")
logger.error("Something went wrong", exc_info=True)

# Add context
logger.set_context(user_id="123", request_id="abc")
logger.info("Processing request")

# Or use context manager
with LoggerContext(logger, module="auth", action="login"):
    logger.info("User logging in")
```

### PromptBuilder

```python
from utils import PromptBuilder, PromptStyle

# Create builder
builder = PromptBuilder(style=PromptStyle.EXPERT)

# Generate code review prompt
prompt = builder.code_review(
    code="def add(a, b): return a + b",
    language="python",
    focus=["performance", "error handling"]
)

# Generate test prompt
prompt = builder.generate_tests(
    code=my_code,
    language="python",
    framework="pytest",
    coverage=80
)

# Custom prompt
prompt = builder.build(
    pattern="expert_system",
    variables={
        "domain": "web development",
        "years": "10+",
        "expertise": "React, TypeScript, Node.js",
        "task": "Build a component library"
    }
)
```

### CodeValidator

```python
from utils import CodeValidator, validate_python_file, scan_for_secrets

# Validate Python code
validator = CodeValidator(strict=False)
code = """
def process(data):
    eval(data)  # Security issue!
    return result
"""
issues = validator.validate_python_code(code)

for issue in issues:
    print(f"{issue.severity.value}: {issue.message}")

# Validate file
issues, summary = validate_python_file("myfile.py")
print(f"Found {summary['total_issues']} issues")

# Scan for secrets
secrets = scan_for_secrets(code)
```

### TemplateEngine

```python
from utils import TemplateEngine, render_template

# Simple rendering
template = "Hello {{name}}, you have {{count}} messages"
output = render_template(template, name="Alice", count=5)

# Conditionals
template = """
{% if is_admin %}
Admin panel available
{% endif %}
"""

# Loops
template = """
{% for item in items %}
- {{item|upper}}
{% endfor %}
"""

# From file
engine = TemplateEngine(template_dir="./templates")
output = engine.render_file("component.jsx", {
    'name': 'Button',
    'props': ['onClick', 'label']
})
```

### ConfigLoader

```python
from utils import ConfigLoader

# Load configuration
loader = ConfigLoader(base_path="./config")
config = loader.load("framework-config.yaml")

# Load multiple with merge
config = loader.load_multiple([
    "framework-config.yaml",
    "user-config.yaml"
], merge=True)

# Get values with dot notation
db_host = loader.get("database.host", default="localhost", config=config)

# Environment variables (in YAML: ${DB_PASSWORD:default})
# Automatically substituted
```

### Context7Client

```python
from integrations import Context7Client

# Initialize client
client = Context7Client(
    cache_enabled=True,
    cache_ttl=3600,
    mappings_file="config/context7-library-mappings.yaml"
)

# Resolve library
library_id = client.resolve_library_id("react")
# Returns: "/facebook/react"

# Get documentation
docs = client.get_library_docs("react", topic="hooks")

# Get multiple libraries
docs = client.get_multiple_libraries(["react", "next.js", "tailwindcss"])

# Search libraries
results = client.search_libraries("state management")

# Cache stats
stats = client.get_cache_stats()
```

---

## Creating Boilerplates

### Structure

```
templates/project-types/my-boilerplate/
├── template.yaml           # Metadata and configuration
├── README.md              # Setup instructions
├── src/                   # Actual source code
│   ├── index.js
│   ├── App.jsx
│   └── components/
├── package.json           # Dependencies
├── .gitignore
└── tsconfig.json
```

### template.yaml Example

```yaml
name: "my-awesome-template"
category: "web_application"
description: "A modern web application template"

default_technologies:
  - react
  - typescript
  - tailwindcss

features:
  - authentication: true
  - routing: true
  - api_integration: true

variables:
  - name: "project_name"
    description: "Project name"
    default: "my-app"

  - name: "author"
    description: "Author name"
    default: "Developer"

files:
  - path: "src/App.tsx"
    template: true  # Will be processed for variables

  - path: "package.json"
    template: true

customization:
  theme:
    default: "light"
    options: ["light", "dark", "auto"]

estimated_time: "3-5 minutes"
```

### Using Variables in Templates

```typescript
// src/App.tsx (template file)
import React from 'react';

function App() {
  return (
    <div>
      <h1>{{project_name}}</h1>
      <p>Created by {{author}}</p>
    </div>
  );
}

export default App;
```

---

## Writing Expert Prompts

### Prompt Template Structure

```markdown
# [Prompt Title]

## Purpose
Clear description of what this prompt does

## Context
When to use this prompt

## Instructions

You are an expert [domain] with extensive experience in [specific areas].

### Task
[Clear task description]

### Requirements
1. Requirement 1
2. Requirement 2
3. Requirement 3

### Best Practices to Follow
- Best practice 1
- Best practice 2
- Best practice 3

## Output Format

Provide your response in the following format:

1. **Analysis**: [Analysis section]
2. **Solution**: [Solution section]
3. **Examples**: [Code examples]
4. **Recommendations**: [Additional recommendations]

## Examples

### Example 1: [Example title]
[Example content]

### Example 2: [Example title]
[Example content]

## Variables

- `{{language}}` - Programming language
- `{{framework}}` - Framework being used
- `{{complexity}}` - Complexity level (simple, moderate, complex)
```

### Example: Code Review Prompt

```markdown
# Expert Code Review

## Purpose
Perform a comprehensive, expert-level code review

## Instructions

You are a senior software engineer with 10+ years of experience in production systems.

### Task
Review the following {{language}} code:

```{{language}}
{{code}}
```

### Review Criteria

1. **Code Quality**
   - Readability and maintainability
   - Naming conventions
   - Code organization

2. **Performance**
   - Time complexity
   - Space complexity
   - Optimization opportunities

3. **Security**
   - Vulnerability assessment
   - Input validation
   - Security best practices

4. **Best Practices**
   - Design patterns
   - SOLID principles
   - Framework-specific conventions

## Output Format

### 🔍 Overall Assessment
[Summary and grade: Excellent/Good/Needs Improvement/Poor]

### ✅ Strengths
- Strength 1
- Strength 2

### ⚠️ Issues Found

#### Critical Issues
1. [Issue with example and fix]

#### Warnings
1. [Issue with suggestion]

#### Suggestions
1. [Optional improvement]

### 💡 Recommendations
[Specific, actionable recommendations]

### 📝 Refactored Code
[Improved version with explanations]
```

---

## Building MCP Handlers

### Handler Template

```python
# File: integrations/mcp_handlers/my_service_handler.py

from typing import Dict, Any, List, Optional
import asyncio

class MyServiceHandler:
    """
    Handler for MyService MCP integration
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize handler

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url', 'https://api.myservice.com')
        self.client = None

    async def connect(self) -> bool:
        """
        Establish connection to service

        Returns:
            True if successful
        """
        # Initialize client
        # Handle authentication
        # Test connection
        return True

    async def list_items(
        self,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List items from service

        Args:
            limit: Maximum items to return
            filters: Optional filters

        Returns:
            List of items
        """
        # Make API call
        # Process response
        # Return data
        return []

    async def create_item(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create new item

        Args:
            data: Item data

        Returns:
            Created item
        """
        # Validate data
        # Make API call
        # Return created item
        return {}

    async def update_item(
        self,
        item_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update existing item

        Args:
            item_id: Item identifier
            data: Updated data

        Returns:
            Updated item
        """
        return {}

    async def delete_item(self, item_id: str) -> bool:
        """
        Delete item

        Args:
            item_id: Item identifier

        Returns:
            True if successful
        """
        return True

    async def close(self):
        """Close connections and cleanup"""
        if self.client:
            await self.client.close()
```

### Registering the Handler

```python
# In execution_engine.py

def _register_mcp_handlers(self) -> Dict[str, Callable]:
    """Register MCP handlers"""
    return {
        'mongodb': self._execute_mongodb_mcp,
        'my_service': self._execute_my_service_mcp,
        # ... other handlers
    }

async def _execute_my_service_mcp(self, task: Task, requirement: Any) -> Any:
    """Execute MyService MCP operations"""
    from integrations.mcp_handlers.my_service_handler import MyServiceHandler

    config = requirement.config or {}
    handler = MyServiceHandler(config)

    try:
        await handler.connect()

        # Execute requested operation
        operation = config.get('operation', 'list')

        if operation == 'list':
            result = await handler.list_items()
        elif operation == 'create':
            result = await handler.create_item(config.get('data', {}))
        # ... other operations

        return {
            'status': 'completed',
            'result': result
        }
    finally:
        await handler.close()
```

---

## Contributing

### Development Workflow

1. **Pick a Task** - Check IMPLEMENTATION_STATUS.md for pending items
2. **Create Branch** - `git checkout -b feature/my-feature`
3. **Implement** - Follow existing patterns
4. **Test** - Add tests for new functionality
5. **Document** - Update relevant documentation
6. **Submit PR** - With clear description

### Code Style

- Follow PEP 8 for Python
- Use type hints
- Add docstrings to all functions
- Keep functions focused and small
- Add comprehensive error handling

### Testing

```python
# tests/test_my_module.py

import pytest
from my_module import MyClass

def test_basic_functionality():
    """Test basic functionality"""
    obj = MyClass()
    result = obj.do_something()
    assert result == expected

@pytest.mark.asyncio
async def test_async_operation():
    """Test async operation"""
    obj = MyClass()
    result = await obj.async_operation()
    assert result is not None
```

---

## Additional Resources

- **CLAUDE.md** - Guide for Claude Code instances
- **ARCHITECTURE.md** - Detailed architecture documentation
- **README.md** - Main project documentation
- **IMPLEMENTATION_STATUS.md** - Current progress and next steps

---

## Support

For questions or issues:
1. Check existing documentation
2. Review examples in `examples/`
3. Check IMPLEMENTATION_STATUS.md for known limitations
4. Create an issue in the repository

---

**Happy Building! 🚀**
