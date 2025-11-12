# Developer Guide: Building with ClaudeOnSteroids

## Table of Contents
1. [Project Overview](#project-overview)
2. [Adding Skills](#adding-skills)
3. [Adding MCP Tools](#adding-mcp-tools)
4. [Creating Applications](#creating-applications)
5. [Project Organization](#project-organization)
6. [Best Practices](#best-practices)

---

## Project Overview

**ClaudeOnSteroids** is an automated development framework that converts natural language into production-ready software through intelligent orchestration.

### Core Architecture

```
Natural Language Request
    ↓
TaskPlanner (analyzes & decomposes)
    ↓
ExecutionEngine (orchestrates)
    ↓
Skills + MCPs + Context7
    ↓
Generated Application
```

### Key Components

1. **Task Planner** - [task_planner.py](task_planner.py)
   - Analyzes natural language
   - Detects technologies
   - Creates execution plan

2. **Execution Engine** - [execution_engine.py](execution_engine.py)
   - Orchestrates execution
   - Manages Skills and MCPs
   - Handles errors and retries

3. **Skills** - Reusable templates at [skills/](skills/)
   - Document generation (docx, pdf, pptx, xlsx)
   - Web development (React, Next.js)
   - Design tools (themes, canvas)

4. **MCPs** - External integrations
   - Database (MongoDB, Airtable)
   - Payment (Stripe)
   - Productivity (Notion, HubSpot)

5. **Context7** - Real-time documentation fetching

---

## Adding Skills

Skills are reusable task templates that extend framework capabilities.

### Skill Structure

```
skills/
└── your-skill-name/
    ├── SKILL.md          # Documentation & usage
    ├── adapter.py        # Python adapter implementation
    ├── templates/        # Code templates (optional)
    └── examples/         # Example outputs (optional)
```

### Step 1: Create Skill Directory

```bash
mkdir -p skills/your-skill-name
cd skills/your-skill-name
```

### Step 2: Write SKILL.md

Create comprehensive documentation:

```markdown
# Your Skill Name

## Overview
Brief description of what this skill does.

## Capabilities
- Feature 1
- Feature 2
- Feature 3

## Prerequisites
- Required dependencies
- Environment setup

## Technologies
- Primary tech stack
- SDKs and libraries

## Usage Examples

### Basic Example
\`\`\`python
# Example code
result = await skill_adapter.execute(task_data)
\`\`\`

### Advanced Example
\`\`\`python
# More complex example
result = await skill_adapter.execute_advanced({
    'option1': 'value1',
    'option2': 'value2'
})
\`\`\`

## Best Practices
- Best practice 1
- Best practice 2

## Resources
- Documentation links
- Tool references
```

**Real Example**: See [skills/stripe/SKILL.md](skills/stripe/SKILL.md) for a comprehensive example.

### Step 3: Implement Adapter

Create `adapter.py`:

```python
"""
Your Skill Name Adapter
Handles task execution for [your skill purpose]
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path

class YourSkillAdapter:
    """Adapter for your skill functionality."""

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the skill adapter.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.output_dir = Path(self.config.get('output_directory', './output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill task.

        Args:
            task_data: Task parameters and configuration

        Returns:
            Dict with execution results
        """
        try:
            # Your implementation here
            result = await self._do_work(task_data)

            return {
                'success': True,
                'output_files': result['files'],
                'metadata': result['metadata']
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def _do_work(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Internal implementation of the skill logic."""
        # Implement your skill logic here
        pass

    async def validate_config(self) -> bool:
        """Validate skill configuration."""
        # Check required config values
        return True

    async def cleanup(self):
        """Cleanup resources if needed."""
        pass
```

### Step 4: Register in skills-manifest.yaml

Add your skill to [skills-manifest.yaml](skills-manifest.yaml):

```yaml
skills:
  your-skill-name:
    name: "Your Skill Name"
    description: "Brief description of skill purpose"
    version: "1.0.0"
    category: "web|document|design|dev|data|automation"

    capabilities:
      - capability_1
      - capability_2
      - capability_3

    keywords:
      - keyword1
      - keyword2
      - keyword3

    requires:
      - python_package_1
      - python_package_2

    config:
      output_directory: "./output"
      option1: "default_value"
      option2: true

    examples:
      - name: "Basic Usage"
        description: "Simple example"
        task: "Generate basic output"

      - name: "Advanced Usage"
        description: "Complex example"
        task: "Generate advanced output with options"
```

### Step 5: Register Handler in Execution Engine

Edit [execution_engine.py](execution_engine.py):

```python
# In ExecutionEngine class

def _register_skill_handlers(self):
    """Register all skill handlers."""

    # ... existing skills ...

    # Your new skill
    from skills.your_skill_name.adapter import YourSkillAdapter
    self.skill_handlers['your-skill-name'] = YourSkillAdapter
```

### Step 6: Add Technology Detection (Optional)

In [task_planner.py](task_planner.py), add technology mapping:

```python
# Around line 180-200 in analyze_request()

tech_skill_mapping = {
    # ... existing mappings ...
    'your-keyword': 'your-skill-name',
    'your-tech': 'your-skill-name',
}
```

### Step 7: Test Your Skill

```bash
# Test standalone
python -c "
import asyncio
from skills.your_skill_name.adapter import YourSkillAdapter

async def test():
    adapter = YourSkillAdapter({'output_directory': './test-output'})
    result = await adapter.execute({'test': 'data'})
    print(result)

asyncio.run(test())
"

# Test via framework
python orchestrator/main.py --task "Use your-skill-name to generate output"
```

---

## Adding MCP Tools

MCPs (Model Context Protocol) enable external service integrations.

### MCP Structure

```
integrations/
└── your_mcp/
    ├── handler.py        # MCP handler implementation
    ├── config.yaml       # MCP configuration
    └── README.md         # Integration docs
```

### Step 1: Define in mcp-registry.yaml

Add MCP definition to [mcp-registry.yaml](mcp-registry.yaml):

```yaml
mcps:
  your-mcp:
    name: "Your Service Name"
    description: "Integration with Your Service"
    version: "1.0.0"
    category: "database|payment|productivity|system|communication"

    requires_docker: false  # or true
    requires_auth: true     # if API keys needed

    capabilities:
      - read_data
      - write_data
      - query_records
      - execute_operations

    connection:
      type: "api|sdk|docker"
      base_url: "https://api.yourservice.com/v1"
      auth_method: "api_key|oauth|basic"

    config:
      timeout: 30
      retry_attempts: 3
      retry_delay: 1

    endpoints:
      list_items:
        method: "GET"
        path: "/items"
        description: "List all items"

      create_item:
        method: "POST"
        path: "/items"
        description: "Create new item"
```

### Step 2: Implement MCP Handler

Create `integrations/your_mcp/handler.py`:

```python
"""
Your MCP Handler
Manages connection and operations for Your Service
"""

import asyncio
import aiohttp
from typing import Dict, Any, List, Optional

class YourMCPHandler:
    """Handler for Your Service MCP integration."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize MCP handler.

        Args:
            config: MCP configuration from registry
        """
        self.config = config
        self.base_url = config.get('connection', {}).get('base_url')
        self.api_key = config.get('api_key')  # From environment or config
        self.session: Optional[aiohttp.ClientSession] = None
        self.connected = False

    async def connect(self) -> bool:
        """
        Establish connection to the service.

        Returns:
            True if connection successful
        """
        try:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
            )

            # Verify connection
            async with self.session.get(f'{self.base_url}/health') as resp:
                if resp.status == 200:
                    self.connected = True
                    return True

            return False

        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    async def disconnect(self):
        """Close connection and cleanup."""
        if self.session:
            await self.session.close()
        self.connected = False

    async def list_items(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        List items from the service.

        Args:
            filters: Optional filters

        Returns:
            List of items
        """
        if not self.connected:
            await self.connect()

        try:
            params = filters or {}
            async with self.session.get(
                f'{self.base_url}/items',
                params=params
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get('items', [])

        except Exception as e:
            print(f"Failed to list items: {e}")
            return []

    async def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new item.

        Args:
            item_data: Item data

        Returns:
            Created item data
        """
        if not self.connected:
            await self.connect()

        try:
            async with self.session.post(
                f'{self.base_url}/items',
                json=item_data
            ) as resp:
                resp.raise_for_status()
                return await resp.json()

        except Exception as e:
            print(f"Failed to create item: {e}")
            return {'error': str(e)}

    async def execute_operation(
        self,
        operation: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a generic operation.

        Args:
            operation: Operation name
            params: Operation parameters

        Returns:
            Operation result
        """
        # Route to appropriate method
        if operation == 'list':
            items = await self.list_items(params.get('filters'))
            return {'items': items}

        elif operation == 'create':
            result = await self.create_item(params.get('data'))
            return result

        # Add more operations as needed

        return {'error': f'Unknown operation: {operation}'}

    async def validate_connection(self) -> bool:
        """Validate the connection is working."""
        try:
            async with self.session.get(f'{self.base_url}/health') as resp:
                return resp.status == 200
        except:
            return False
```

### Step 3: Register in Execution Engine

Edit [execution_engine.py](execution_engine.py):

```python
# In ExecutionEngine class

def _register_mcp_handlers(self):
    """Register all MCP handlers."""

    # ... existing MCPs ...

    # Your new MCP
    from integrations.your_mcp.handler import YourMCPHandler
    self.mcp_handlers['your-mcp'] = YourMCPHandler

async def _execute_your_mcp(
    self,
    task: 'Task',
    handler: YourMCPHandler
) -> Dict[str, Any]:
    """
    Execute Your MCP task.

    Args:
        task: Task to execute
        handler: MCP handler instance

    Returns:
        Execution result
    """
    try:
        # Connect
        await handler.connect()

        # Extract operation and params from task
        operation = task.params.get('operation', 'list')
        params = task.params.get('params', {})

        # Execute
        result = await handler.execute_operation(operation, params)

        return {
            'success': True,
            'data': result,
            'task_id': task.id
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'task_id': task.id
        }

    finally:
        await handler.disconnect()
```

### Step 4: Add Technology Detection

In [task_planner.py](task_planner.py):

```python
# Around line 170-190

tech_mcp_mapping = {
    # ... existing mappings ...
    'yourservice': 'your-mcp',
    'your-keyword': 'your-mcp',
}
```

### Step 5: Test MCP Integration

```bash
# Test handler directly
python -c "
import asyncio
from integrations.your_mcp.handler import YourMCPHandler

async def test():
    handler = YourMCPHandler({
        'connection': {'base_url': 'https://api.yourservice.com/v1'},
        'api_key': 'your-test-key'
    })

    await handler.connect()
    items = await handler.list_items()
    print(f'Found {len(items)} items')
    await handler.disconnect()

asyncio.run(test())
"

# Test via framework
python orchestrator/main.py --task "Use your-mcp to list items"
```

---

## Creating Applications

### Quick Start

```bash
# Interactive mode
python orchestrator/main.py

# Single task
python orchestrator/main.py --task "Create a React dashboard with MongoDB"

# With custom output
python orchestrator/main.py \
  --task "Build Next.js SaaS app" \
  --output-dir ./my-app \
  --include-tests
```

### Application Templates

The framework includes production-ready templates in [templates/](templates/):

#### Available Templates

1. **Next.js SaaS** - Full-stack SaaS application
   - Authentication
   - Stripe payments
   - MongoDB database
   - Dashboard UI

2. **React Dashboard** - Admin dashboard
   - Charts and analytics
   - Data tables
   - Responsive design

3. **FastAPI Backend** - Python API
   - REST endpoints
   - Authentication
   - Database integration

4. **Express.js API** - Node.js API
   - RESTful routes
   - Middleware
   - Database models

5. **Python CLI Tool** - Command-line application
   - Argument parsing
   - Configuration
   - Logging

6. **Chrome Extension** - Browser extension
   - Popup UI
   - Background scripts
   - Content scripts

7. **Vue.js SPA** - Single-page application
   - Routing
   - State management
   - Component library

### Creating Custom Templates

1. **Create Template Directory**

```bash
mkdir -p templates/project-types/your-template
cd templates/project-types/your-template
```

2. **Create Template Files**

```
your-template/
├── template.yaml        # Template configuration
├── files/              # Template files
│   ├── src/
│   ├── package.json
│   └── README.md
└── SKILL.md            # Template documentation
```

3. **Define template.yaml**

```yaml
name: "Your Template Name"
description: "Brief description"
version: "1.0.0"
category: "web|api|mobile|cli|automation"

technologies:
  - tech1
  - tech2
  - tech3

features:
  - feature1
  - feature2

structure:
  - path: "src/"
    type: "directory"

  - path: "src/index.js"
    type: "file"
    template: "files/src/index.js"

  - path: "package.json"
    type: "file"
    template: "files/package.json"

scripts:
  install: "npm install"
  dev: "npm run dev"
  build: "npm run build"
  test: "npm test"

environment:
  - key: "API_KEY"
    description: "API key for service"
    required: true

  - key: "DATABASE_URL"
    description: "Database connection string"
    required: false
```

4. **Use Template**

```bash
python orchestrator/main.py --task "Create app using your-template"
```

### Example Workflows

#### 1. SaaS Application

```bash
python orchestrator/main.py --task "
Create a SaaS application with:
- Next.js frontend
- Stripe subscription billing
- MongoDB database
- User authentication
- Admin dashboard
- Email notifications
"
```

#### 2. API Integration

```bash
python orchestrator/main.py --task "
Build API that:
- Syncs Notion to MongoDB
- Sends Stripe invoices
- Generates PDF reports
- Posts to Slack
"
```

#### 3. Document Automation

```bash
python orchestrator/main.py --task "
Automate documents:
- Fetch data from Airtable
- Generate branded PowerPoint
- Create Excel reports
- Email to stakeholders
"
```

#### 4. Data Pipeline

```bash
python orchestrator/main.py --task "
Create ETL pipeline:
- Extract from multiple MongoDB collections
- Transform with validation
- Load to data warehouse
- Generate analytics dashboard
"
```

---

## Project Organization

### Directory Structure

```
ClaudeOnSteroids/
├── orchestrator/              # Core framework
│   ├── main.py               # CLI entry point
│   ├── task_planner.py       # Task planning
│   ├── execution_engine.py   # Execution orchestration
│   └── __init__.py
│
├── integrations/             # MCP integrations
│   ├── context7_client.py    # Context7 integration
│   ├── mongodb/              # MongoDB MCP
│   ├── stripe/               # Stripe MCP
│   └── notion/               # Notion MCP
│
├── skills/                   # Skill adapters
│   ├── docx/                 # Word documents
│   ├── pdf/                  # PDF generation
│   ├── stripe/               # Stripe skill
│   └── postgresql/           # PostgreSQL skill
│
├── templates/                # Project templates
│   ├── project-types/        # Application templates
│   │   ├── nextjs-saas/
│   │   ├── react-dashboard/
│   │   └── fastapi-backend/
│   └── components/           # Reusable components
│
├── config/                   # Configuration
│   ├── framework-config.yaml # Main config
│   ├── mcp-registry.yaml     # MCP definitions (DEPRECATED)
│   └── skills-manifest.yaml  # Skills catalog (DEPRECATED)
│
├── utils/                    # Utilities
│   ├── file_manager.py       # File operations
│   ├── validator.py          # Validation
│   └── logger.py             # Logging
│
├── examples/                 # Example projects
│   ├── portfolio-management-system/
│   └── stripe-crypto-onramp/
│
├── gitbook/                  # Documentation
│   ├── getting-started/
│   ├── core-concepts/
│   ├── development/
│   └── examples/
│
├── memory-bank/              # AI context
│   ├── Active Context.md
│   ├── Project Brief.md
│   ├── Tech Context.md
│   └── System Patterns.md
│
├── workspace/                # Build workspace
│   └── [generated-projects]/
│
├── output/                   # Final outputs
│   └── [completed-projects]/
│
├── .mcp.json                 # MCP server config
├── requirements.txt          # Python dependencies
├── setup.py                  # Setup script
├── CLAUDE.md                 # AI instructions
├── DEVELOPER_GUIDE.md        # This file
└── README.md                 # Main documentation
```

### File Naming Conventions

- **Python files**: `snake_case.py`
- **Configuration**: `kebab-case.yaml`
- **Documentation**: `SCREAMING_SNAKE_CASE.md` or `Title Case.md`
- **Templates**: `kebab-case/`
- **Components**: `PascalCase.tsx` (React) or `kebab-case.vue` (Vue)

### Code Organization Best Practices

1. **One responsibility per file**
   - Each module should have a clear, single purpose
   - Example: `task_planner.py` only handles planning

2. **Clear separation of concerns**
   - Planning → Execution → Integration
   - No circular dependencies

3. **Consistent error handling**
   - Try/except at handler level
   - Return structured error objects
   - Log errors with context

4. **Type hints everywhere**
   ```python
   async def execute_task(
       self,
       task: Task,
       context: ExecutionContext
   ) -> Dict[str, Any]:
       ...
   ```

5. **Comprehensive docstrings**
   ```python
   """
   Execute a task with retry logic.

   Args:
       task: Task to execute
       context: Execution context

   Returns:
       Dict with execution results

   Raises:
       ExecutionError: If all retries fail
   """
   ```

---

## Best Practices

### Skill Development

1. **Keep adapters stateless**
   - Don't store state between executions
   - Use ExecutionContext for shared state

2. **Return file paths**
   ```python
   return {
       'success': True,
       'output_files': [
           str(output_file1),
           str(output_file2)
       ],
       'metadata': {...}
   }
   ```

3. **Validate inputs**
   ```python
   async def execute(self, task_data: Dict[str, Any]):
       required = ['param1', 'param2']
       for param in required:
           if param not in task_data:
               raise ValueError(f'Missing required param: {param}')
   ```

4. **Handle errors gracefully**
   ```python
   try:
       result = await self._do_work(task_data)
   except SpecificError as e:
       # Handle specific error
       return {'success': False, 'error': str(e)}
   except Exception as e:
       # Handle general error
       return {'success': False, 'error': f'Unexpected error: {e}'}
   ```

5. **Use async/await consistently**
   - All handlers should be async
   - Use aiohttp for HTTP requests
   - Use asyncio for concurrent operations

### MCP Development

1. **Connection management**
   ```python
   async def connect(self) -> bool:
       """Establish connection and verify."""
       try:
           # Connect
           self.client = await create_client()
           # Verify
           await self.client.ping()
           self.connected = True
           return True
       except:
           return False
   ```

2. **Implement retries**
   ```python
   async def execute_with_retry(
       self,
       operation: callable,
       max_retries: int = 3
   ):
       for attempt in range(max_retries):
           try:
               return await operation()
           except TransientError:
               if attempt == max_retries - 1:
                   raise
               await asyncio.sleep(2 ** attempt)  # Exponential backoff
   ```

3. **Clean resource usage**
   ```python
   async def __aenter__(self):
       await self.connect()
       return self

   async def __aexit__(self, *args):
       await self.disconnect()
   ```

4. **Validate responses**
   ```python
   async def fetch_data(self) -> List[Dict]:
       response = await self.client.get('/data')

       if not response.ok:
           raise APIError(f'Failed: {response.status}')

       data = await response.json()

       if not isinstance(data, list):
           raise ValidationError('Expected list response')

       return data
   ```

### Template Development

1. **Parameterize everything**
   - Use template variables: `{{ project_name }}`
   - Allow customization via config

2. **Include documentation**
   - README.md with setup instructions
   - Code comments explaining key parts
   - Example .env file

3. **Follow conventions**
   - Standard directory structure
   - Consistent naming
   - Industry best practices

4. **Make it runnable**
   - Include package.json / requirements.txt
   - Add npm scripts / Make targets
   - Provide development server

5. **Add tests**
   - Unit tests for core logic
   - Integration tests for APIs
   - E2E tests for critical flows

### Documentation

1. **Keep SKILL.md comprehensive**
   - Overview
   - Prerequisites
   - Usage examples
   - Best practices
   - Resources

2. **Document all public methods**
   ```python
   async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Execute the skill task.

       This method handles the main execution logic for the skill...

       Args:
           task_data: Dictionary containing:
               - param1 (str): Description
               - param2 (int): Description

       Returns:
           Dictionary with:
               - success (bool): Execution status
               - output_files (List[str]): Generated files
               - metadata (Dict): Additional info

       Raises:
           ValueError: If required params missing
           ExecutionError: If execution fails
       """
   ```

3. **Update configuration docs**
   - Document all config options
   - Provide examples
   - Explain defaults

4. **Maintain examples**
   - Keep examples current
   - Test examples regularly
   - Show both basic and advanced usage

### Testing

1. **Test skills standalone**
   ```python
   import asyncio
   from skills.your_skill.adapter import YourSkillAdapter

   async def test():
       adapter = YourSkillAdapter()
       result = await adapter.execute({'test': 'data'})
       assert result['success']
       print('✅ Skill test passed')

   asyncio.run(test())
   ```

2. **Test MCPs with mocks**
   ```python
   import unittest
   from unittest.mock import AsyncMock, patch

   class TestYourMCP(unittest.TestCase):
       @patch('aiohttp.ClientSession')
       async def test_list_items(self, mock_session):
           # Setup mock
           mock_response = AsyncMock()
           mock_response.json.return_value = {'items': []}
           mock_session.get.return_value.__aenter__.return_value = mock_response

           # Test
           handler = YourMCPHandler(config)
           items = await handler.list_items()

           # Assert
           self.assertEqual(len(items), 0)
   ```

3. **Test via framework**
   ```bash
   # Dry run to see plan
   python orchestrator/main.py \
     --task "Use your-skill" \
     --dry-run

   # Execute test task
   python orchestrator/main.py \
     --task "Use your-skill with test data" \
     --output-dir ./test-output
   ```

### Performance

1. **Use parallel execution**
   ```python
   # In task planner
   tasks = [
       Task(id='1', type=TaskType.API_INTEGRATION),
       Task(id='2', type=TaskType.CODE_GENERATION),  # No dependency
       Task(id='3', type=TaskType.TESTING, dependencies=['1', '2'])
   ]
   # Tasks 1 and 2 run in parallel
   ```

2. **Cache expensive operations**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def get_documentation(library: str) -> str:
       # Expensive Context7 call
       pass
   ```

3. **Stream large files**
   ```python
   async def process_large_file(file_path: Path):
       async with aiofiles.open(file_path, 'r') as f:
           async for line in f:
               await process_line(line)
   ```

4. **Batch operations**
   ```python
   # Instead of:
   for item in items:
       await api.create(item)

   # Do:
   await api.batch_create(items)
   ```

### Security

1. **Never commit secrets**
   - Use environment variables
   - Add to .gitignore
   - Use .env.example as template

2. **Validate inputs**
   ```python
   def sanitize_filename(filename: str) -> str:
       # Remove dangerous characters
       safe = re.sub(r'[^\w\-.]', '', filename)
       # Prevent path traversal
       return Path(safe).name
   ```

3. **Use secure connections**
   ```python
   async with aiohttp.ClientSession() as session:
       # Always use HTTPS
       async with session.get('https://api.service.com') as resp:
           ...
   ```

4. **Implement rate limiting**
   ```python
   from asyncio import Semaphore

   semaphore = Semaphore(10)  # Max 10 concurrent requests

   async def api_call():
       async with semaphore:
           # Make request
           pass
   ```

---

## Quick Reference

### Common Commands

```bash
# Setup
python setup.py

# Run framework
python orchestrator/main.py

# Single task
python orchestrator/main.py --task "description"

# Dry run (show plan)
python orchestrator/main.py --task "..." --dry-run

# With tests
python orchestrator/main.py --task "..." --include-tests

# Custom output
python orchestrator/main.py --task "..." --output-dir ./my-app

# Debug mode
python orchestrator/main.py --log-level DEBUG --task "..."
```

### File Locations

- **Skills**: `skills/your-skill/`
- **MCPs**: `integrations/your-mcp/` or configured in `.mcp.json`
- **Templates**: `templates/project-types/your-template/`
- **Config**: `config/` or root
- **Output**: `./output/` (configurable)
- **Workspace**: `./workspace/` (temporary)

### Key Files

- [task_planner.py](task_planner.py) - Task planning logic
- [execution_engine.py](execution_engine.py) - Execution orchestration
- [skills-manifest.yaml](skills-manifest.yaml) - Skills registry (DEPRECATED - now in SKILL.md)
- [.mcp.json](.mcp.json) - MCP server configuration
- [CLAUDE.md](CLAUDE.md) - AI instructions

### Getting Help

1. Check [README.md](README.md) for overview
2. Read [gitbook/](gitbook/) documentation
3. Review [examples/](examples/) for real applications
4. See [CLAUDE.md](CLAUDE.md) for implementation details

---

## What's Next?

1. **Explore Examples**
   - [Portfolio Management System](examples/portfolio-management-system/)
   - [Stripe Crypto Onramp](examples/stripe-crypto-onramp/)

2. **Read Documentation**
   - [Getting Started](gitbook/getting-started/)
   - [Core Concepts](gitbook/core-concepts/)
   - [Development Guides](gitbook/development/)

3. **Build Something**
   ```bash
   python orchestrator/main.py --task "Your amazing idea"
   ```

---

**Happy Building! 🚀**

*Last Updated: November 12, 2025*
