# Tech Context

## Dependencies

### Core Python Dependencies

**From `requirements.txt`:**

```python
# Core dependencies
pyyaml>=6.0.1           # YAML configuration parsing
asyncio>=3.4.3          # Async/await support (built-in, but version noted)
pathlib>=1.0.1          # Path handling (built-in)

# Logging and monitoring
python-json-logger>=2.0.7  # Structured JSON logging

# Optional: Web scraping (if using web tools)
requests>=2.31.0        # HTTP requests
beautifulsoup4>=4.12.2  # HTML parsing

# Optional: Data processing
pandas>=2.0.0           # Data manipulation

# Optional: Document generation (if not using skills)
python-docx>=1.1.0      # Word document generation
reportlab>=4.0.0        # PDF generation
openpyxl>=3.1.2         # Excel file handling

# Optional: Testing
pytest>=7.4.0           # Test framework
pytest-asyncio>=0.21.0  # Async test support

# Optional: Code quality
black>=23.0.0           # Code formatter
flake8>=6.0.0          # Linter
mypy>=1.5.0            # Type checker

# Development dependencies
setuptools>=68.0.0      # Package building
wheel>=0.41.0           # Package distribution
```

### External Integrations

**MCPs (Model Context Protocol):**
- MongoDB (via Docker)
- Stripe (via Docker)
- Notion (via Docker)
- Airtable (API key required)
- HubSpot (API key required)
- Filesystem (local)
- Chrome Control (local)
- Mac Control (local)
- Beeper Desktop (local)
- Context7 (API)
- YouTube (via Docker)
- Web Search/Fetch (APIs)

**Skills:**
- Located at `/mnt/skills/` (public and examples)
- Document skills: docx, pdf, pptx, xlsx
- Web skills: artifacts-builder
- Design skills: theme-factory, canvas-design
- Dev skills: mcp-builder, skill-creator
- AI/ML skills: ml-model-deployer, data-analyzer
- Testing: test-generator
- DevOps: docker-composer, ci-cd-builder
- Database: database-modeler

**Context7 Libraries (100+ mappings):**
- Frontend: React, Next.js, Vue, Svelte, Angular
- Backend: Express, FastAPI, Django, Flask, NestJS
- Databases: MongoDB, PostgreSQL, Redis, Prisma
- Payment: Stripe, PayPal
- UI: Tailwind, Material-UI, Chakra, Ant Design
- State: Redux, Zustand, Recoil, Pinia
- Testing: Jest, Vitest, Pytest, Playwright, Cypress
- Build: Vite, Webpack, esbuild, Turbopack

## Build Tools

### Python Environment

**Setup:**
```bash
python setup.py          # Automated setup
pip install -r requirements.txt  # Manual install
```

**Python Version:**
- Minimum: Python 3.8+
- Recommended: Python 3.11+

### Development Tools

**Code Formatting:**
- **Black** (Python): Configured in framework-config.yaml
- **Prettier** (JavaScript/TypeScript): For boilerplate templates

**Linting:**
- **Flake8** (Python): Style and error checking
- **ESLint** (JavaScript/TypeScript): For templates

**Type Checking:**
- **mypy** (Python): Static type analysis
- **TypeScript** (JavaScript): Built-in type checking

**Testing:**
- **pytest**: Python testing framework
- **pytest-asyncio**: Async test support
- Test coverage: 80% threshold (configured)

### Build System

**No Traditional Build Step:**
- Framework runs directly as Python scripts
- Templates are generated at runtime
- No compilation step required

**Template Generation:**
- Jinja2-style template engine
- Variable substitution
- Conditional rendering
- Loop support

## Environment Constraints

### Required Environment

**System Requirements:**
- **OS**: macOS, Linux, Windows (with WSL)
- **Python**: 3.8+ with pip
- **Docker**: Required for MongoDB, Stripe, Notion, YouTube MCPs
- **Git**: For version control (optional)

**Disk Space:**
- Framework: ~50MB
- Workspace: Variable (depends on projects)
- Cache: Up to 1GB (configurable)
- Output: Variable (depends on projects)

### Environment Variables

**Configuration via Environment:**
```bash
# Framework settings
BYTECLAUDE_WORK_DIR=./workspace
BYTECLAUDE_OUTPUT_DIR=./output
BYTECLAUDE_LOG_LEVEL=INFO

# MCP Credentials (examples)
MONGODB_CONNECTION_STRING=mongodb://...
STRIPE_API_KEY=sk_...
AIRTABLE_API_KEY=pat_...
HUBSPOT_API_KEY=...

# Context7 (if needed)
CONTEXT7_API_KEY=...
```

**Security:**
- Never commit API keys to repository
- Use `.env` files (gitignored)
- Environment variable substitution in config

### Docker Requirements

**MCPs Requiring Docker:**
- MongoDB: Database operations
- Stripe: Payment processing (test mode available)
- Notion: Workspace management
- YouTube: Transcript extraction

**Docker Setup:**
```bash
# MongoDB
docker run -d -p 27017:27017 mongo

# Stripe (test mode)
docker run -d -p 4242:4242 stripe/stripe-cli

# Notion
docker run -d notion-mcp

# YouTube
docker run -d youtube-mcp
```

### File System Constraints

**Skills Location:**
- Primary: `/mnt/skills/` (expected location)
- Fallback: `./skills` (local fallback configured)

**Directory Permissions:**
- Framework needs read/write access to:
  - `./workspace/` (working directory)
  - `./output/` (output directory)
  - `./cache/` (cache directory)
  - `./logs/` (log directory)

**File Size Limits:**
- Max file size: 100MB (configurable)
- Allowed extensions: .js, .jsx, .ts, .tsx, .py, .md, .json, .yaml, etc.

### Network Requirements

**External Services:**
- Context7 API: For documentation retrieval
- MCP APIs: Various external services
- Web Search/Fetch: Internet access required

**Rate Limiting:**
- Context7: 60 requests per minute (configurable)
- MCPs: Service-specific limits
- Caching: Enabled to reduce API calls

### Performance Constraints

**Parallel Execution:**
- Default: 5 concurrent tasks
- Configurable: `framework.max_parallel_tasks`
- Resource-aware: Adjusts based on system capacity

**Memory Usage:**
- Framework: ~50-100MB base
- Per task: Variable (depends on complexity)
- Cache: Up to 1GB (configurable)

**Timeout Settings:**
- Per task: 600 seconds (10 minutes, configurable)
- MCP requests: 60 seconds (configurable)
- Context7 requests: 30 seconds (configurable)

## Technology Stack Summary

### Core Stack
- **Language**: Python 3.8+
- **Async**: asyncio (built-in)
- **Config**: YAML (PyYAML)
- **Logging**: Python logging + JSON logger

### Integration Stack
- **MCP Protocol**: Model Context Protocol
- **Skills**: Markdown-based skill definitions
- **Context7**: REST API for documentation
- **Docker**: Container runtime for MCPs

### Template Stack
- **Template Engine**: Custom Jinja2-style engine
- **Boilerplates**: Production-ready code templates
- **Languages**: TypeScript, JavaScript, Python, Java, Go, Rust, etc.

### Development Stack
- **Testing**: pytest, pytest-asyncio
- **Formatting**: Black, Prettier
- **Linting**: Flake8, ESLint
- **Type Checking**: mypy, TypeScript

## Compatibility Matrix

### Operating Systems
- ✅ macOS (darwin) - Fully supported
- ✅ Linux - Fully supported
- ⚠️ Windows - Supported via WSL (Docker requirement)

### Python Versions
- ✅ Python 3.8 - Minimum supported
- ✅ Python 3.9 - Fully supported
- ✅ Python 3.10 - Fully supported
- ✅ Python 3.11 - Recommended
- ✅ Python 3.12 - Fully supported

### Docker
- ✅ Docker Desktop (macOS/Windows)
- ✅ Docker Engine (Linux)
- ⚠️ Docker Compose - Optional (for MCP orchestration)

