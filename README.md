# Automated Microsoftware Development Framework
## Claude Code + Skills + MCPs + Context7 Integration

### Overview
This framework provides a fully automated development environment that combines:
- **Claude Code**: Agentic coding capabilities
- **Skills**: Pre-built task templates and workflows
- **MCPs**: External integrations (Notion, MongoDB, Stripe, Airtable, etc.)
- **Context7**: Dynamic library documentation access
- **TaskMaster**: Intelligent task orchestration and management

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Task Orchestrator                         │
│  (Interprets requirements → Plans → Executes → Validates)   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐            ┌─────▼──────┐
   │  Skills  │            │   Context7  │
   │  Engine  │            │   Resolver  │
   └────┬─────┘            └─────┬───────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │    Claude Code Core     │
        │  (Execution Environment) │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │      MCP Integration    │
        │  Layer (Tool Calling)   │
        └─────────────────────────┘
```

### Key Features

1. **Intelligent Task Decomposition**
   - Natural language to structured tasks
   - Automatic dependency resolution
   - Parallel execution optimization

2. **Context-Aware Development**
   - Dynamic documentation retrieval via Context7
   - Best practices from Skills library
   - Real-time API integration via MCPs

3. **Multi-Domain Support**
   - Web applications (React, Next.js, etc.)
   - API integrations (Stripe, Notion, Airtable)
   - Database operations (MongoDB)
   - Document generation (DOCX, PPTX, PDF, XLSX)
   - File system operations

4. **Quality Assurance**
   - Automated testing integration
   - Code review checkpoints
   - Documentation generation

### Directory Structure

```
automated-dev-framework/
├── config/
│   ├── framework-config.yaml       # Main configuration
│   ├── mcp-registry.yaml          # Available MCPs
│   └── skills-manifest.yaml       # Skills catalog
├── orchestrator/
│   ├── task_planner.py            # Task decomposition
│   ├── execution_engine.py        # Workflow execution
│   ├── context_manager.py         # Context7 integration
│   └── skill_resolver.py          # Skills selection
├── templates/
│   ├── project-types/             # Project scaffolds
│   ├── workflows/                 # Common workflows
│   └── prompts/                   # Optimized prompts
├── integrations/
│   ├── mcp_handlers/              # MCP-specific logic
│   ├── skill_adapters/            # Skills integration
│   └── context7_client/           # Context7 API wrapper
├── utils/
│   ├── file_manager.py            # File operations
│   ├── validation.py              # Quality checks
│   └── logger.py                  # Execution tracking
└── examples/
    ├── full-stack-app/            # Example projects
    ├── data-pipeline/
    └── document-automation/

```

### Quick Start

#### 1. Installation
```bash
# Clone the framework
git clone <repo-url>
cd automated-dev-framework

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configuration
```bash
# Configure your MCPs and API keys
cp config/framework-config.yaml.example config/framework-config.yaml
# Edit with your settings
```

#### 3. Run Your First Automated Project
```bash
# Natural language command
python orchestrator/main.py "Create a React dashboard with Stripe integration"
```

### Usage Examples

#### Example 1: Full-Stack Application
```bash
python orchestrator/main.py \
  --task "Build a Next.js app with MongoDB backend and Stripe payments" \
  --output-dir ./my-app \
  --include-tests
```

#### Example 2: Document Generation Pipeline
```bash
python orchestrator/main.py \
  --task "Generate monthly reports from Airtable data as PDFs" \
  --schedule "0 0 1 * *"
```

#### Example 3: API Integration
```bash
python orchestrator/main.py \
  --task "Sync Notion database with MongoDB and send Slack notifications" \
  --use-skills notion,mongodb,slack
```

### Available MCPs

Your current setup includes:
- **HubSpot**: CRM operations, search, data management
- **Chrome Control**: Browser automation
- **Mac Control**: System automation (osascript)
- **Beeper Desktop**: Messaging integration
- **Filesystem**: File operations
- **Airtable**: Database operations
- **Notion**: Workspace management (via Docker)
- **MongoDB**: Database operations (via Docker)
- **Stripe**: Payment processing (via Docker)
- **Context7**: Library documentation
- **YouTube**: Transcript extraction (via Docker)
- **Web Tools**: Search and fetch

### Skills Catalog

Available skills in your environment:
- **docx**: Document creation and editing
- **pdf**: PDF manipulation and generation
- **pptx**: Presentation creation
- **xlsx**: Spreadsheet operations
- **skill-creator**: Meta-skill for creating new skills
- **product-self-knowledge**: Claude product information
- **artifacts-builder**: Complex web artifacts
- **theme-factory**: Design theming
- **mcp-builder**: MCP server creation
- **canvas-design**: Visual design generation

### Configuration

#### framework-config.yaml
```yaml
framework:
  version: "1.0.0"
  claude_code_enabled: true
  max_parallel_tasks: 5
  
context7:
  enabled: true
  cache_documentation: true
  cache_ttl: 3600

mcps:
  auto_discover: true
  registry_path: "./config/mcp-registry.yaml"

skills:
  base_path: "/mnt/skills"
  auto_load: true
  manifest_path: "./config/skills-manifest.yaml"

execution:
  work_directory: "./workspace"
  output_directory: "./output"
  log_level: "INFO"
  save_checkpoints: true

validation:
  run_tests: true
  code_review: true
  generate_docs: true
```

### Workflow Execution

The framework follows this execution pattern:

1. **Input Processing**
   - Parse natural language request
   - Extract requirements and constraints
   - Identify required capabilities

2. **Planning Phase**
   - Decompose into subtasks
   - Resolve dependencies
   - Select appropriate Skills and MCPs
   - Fetch relevant documentation via Context7

3. **Execution Phase**
   - Execute tasks in optimal order
   - Handle errors and retries
   - Maintain execution state
   - Generate intermediate outputs

4. **Validation Phase**
   - Run automated tests
   - Validate outputs
   - Generate documentation
   - Create deliverables

5. **Delivery Phase**
   - Package outputs
   - Generate reports
   - Archive artifacts

### Advanced Features

#### Custom Workflows
```python
# Define custom workflow
from orchestrator import Workflow

workflow = Workflow("my-custom-flow")
workflow.add_task("setup", use_skills=["skill-creator"])
workflow.add_task("develop", depends_on="setup", use_mcps=["mongodb"])
workflow.add_task("deploy", depends_on="develop")
workflow.execute()
```

#### Context7 Integration
```python
# Automatic documentation retrieval
from integrations.context7_client import Context7Client

client = Context7Client()
# Framework automatically resolves and fetches docs
docs = client.get_docs_for_library("next.js", topic="routing")
```

#### MCP Chaining
```python
# Chain multiple MCP operations
pipeline = MCPPipeline()
pipeline.add_step("airtable", "list_records", base_id="...")
pipeline.add_step("mongodb", "insert_many", transform=custom_transform)
pipeline.add_step("notion", "create_page", map_fields=field_mapping)
pipeline.execute()
```

### Best Practices

1. **Task Definition**: Be specific but flexible in task descriptions
2. **Error Handling**: Framework includes automatic retry logic
3. **Resource Management**: Tasks are optimized for parallel execution
4. **Documentation**: Auto-generated docs for all created software
5. **Testing**: Integrated test generation and execution

### Troubleshooting

Common issues and solutions:
- **MCP Connection Errors**: Check Docker containers are running
- **Skill Not Found**: Verify skills manifest is up to date
- **Context7 Rate Limits**: Enable caching in config
- **Execution Timeout**: Adjust max_parallel_tasks or task complexity

### Contributing

This framework is designed to be extended:
- Add new MCPs in `integrations/mcp_handlers/`
- Create custom skills in `/mnt/skills/user/`
- Define workflow templates in `templates/workflows/`

### License

MIT License

### Support

For issues and questions:
- Documentation: https://docs.claude.com
- Claude Code: https://docs.claude.com/en/docs/claude-code

---

**Version**: 1.0.0  
**Last Updated**: November 2, 2025  
**Powered by**: Claude Sonnet 4.5, Claude Code, Anthropic MCPs
