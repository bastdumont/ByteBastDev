# Installation & Setup

Complete guide to installing and configuring ByteClaude.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **pip**: Package manager (included with Python)
- **RAM**: 4GB (8GB+ recommended)
- **Disk Space**: 2GB for installation + project output

### Optional Requirements
- **Node.js 18+** - For web development templates
- **Docker** - For MongoDB, Notion, and Stripe MCPs
- **Git** - For version control

## Step-by-Step Installation

### 1. Clone the Repository

```bash
# Clone ByteClaude
git clone https://github.com/bastdumont/BalderFrameWork.git

# Navigate to directory
cd BalderFrameWork

# Verify you're in the right place
ls -la  # Should see: orchestrator/, config/, utils/, etc.
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)
python --version
```

### 3. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually:
pip install PyYAML
```

### 4. Run Setup Script

```bash
# Run setup
python setup.py

# This will:
# ✓ Create necessary directories
# ✓ Verify configuration
# ✓ Set up logging
# ✓ Validate installation
```

### 5. Verify Installation

```bash
# Check version
python orchestrator/main.py --version

# Check help
python orchestrator/main.py --help

# Should display help without errors
```

✅ Installation complete!

## Project Structure

After installation, you'll have:

```
BalderFrameWork/
├── orchestrator/                 # Core framework
│   ├── main.py                  # CLI entry point
│   ├── task_planner.py          # Task planning engine
│   └── execution_engine.py      # Execution orchestrator
├── integrations/                # External integrations
│   ├── context7_client.py       # Documentation client
│   ├── mcp_handlers/            # MCP handlers
│   └── skill_adapters/          # Skill adapters
├── utils/                        # Utility modules
├── config/                       # Configuration files
│   ├── framework-config.yaml    # Main configuration
│   ├── mcp-registry.yaml        # MCP definitions
│   └── skills-manifest.yaml     # Skills catalog
├── templates/                    # Boilerplate templates
├── examples/                     # Examples and tutorials
├── workspace/                    # Working directory (created at runtime)
└── output/                       # Generated projects (created at runtime)
```

## Configuration

### Main Configuration File

Edit `config/framework-config.yaml` to customize:

```yaml
# Framework settings
framework:
  max_parallel_tasks: 5          # Increase for faster execution
  enable_checkpoints: true        # Resume on failure
  verbose_logging: false          # Set to true for debugging

# Execution settings
execution:
  work_directory: ./workspace
  output_directory: ./output
  continue_on_error: false
  max_retries: 3

# Context7 settings
context7:
  enabled: true
  cache_ttl: 3600                # Cache for 1 hour
  max_tokens_per_query: 10000

# Validation settings
validation:
  run_tests: true
  code_review: true
  test_coverage_threshold: 80
```

### Environment Variables

Create `.env` file (optional):

```bash
# API Keys
NOTION_API_KEY=your_notion_key
STRIPE_API_KEY=your_stripe_key
HUBSPOT_API_KEY=your_hubspot_key

# Database
MONGODB_URI=mongodb://localhost:27017

# Framework
BYTECLAUDE_LOG_LEVEL=INFO
BYTECLAUDE_DEBUG=false
```

## First Run

### Interactive Mode

```bash
python orchestrator/main.py
```

You'll be prompted for:
1. Project description
2. Technologies to use
3. Output directory

### Batch Mode

```bash
python orchestrator/main.py \
  --task "Your project description" \
  --output-dir ./my-project
```

## Advanced Setup

### Using with Claude Code

To use ByteClaude with Claude Code:

```bash
# Generate execution plan
python orchestrator/main.py \
  --task "Your description" \
  --dry-run > plan.yaml

# Share plan with Claude Code
# Claude Code can then implement based on the plan
```

### Docker Setup

If you want to use Docker-dependent MCPs:

```bash
# Install Docker Desktop from docker.com
docker --version

# Start Docker service
# The framework will automatically use available Docker MCPs
```

### Development Setup

For contributing to ByteClaude:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 orchestrator/ integrations/ utils/

# Run type checker
mypy orchestrator/ integrations/ utils/
```

## Troubleshooting Installation

### Python Version Issue

```bash
# Check Python version
python --version

# If you need Python 3.8+, install it:
# macOS:
brew install python@3.11

# Or use pyenv:
pyenv install 3.11.0
pyenv global 3.11.0
```

### Permission Denied

```bash
# Make scripts executable
chmod +x setup.py
chmod +x orchestrator/main.py

# Reinstall with sudo if needed
sudo pip install -r requirements.txt
```

### Module Import Error

```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Path Issues

```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/BalderFrameWork"

# Verify
python -c "import orchestrator; print(orchestrator.__file__)"
```

## Updating ByteClaude

```bash
# Pull latest changes
git pull origin master

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify update
python orchestrator/main.py --version
```

## Optional: IDE Setup

### VS Code

1. Install Python extension
2. Select interpreter: Command Palette → Python: Select Interpreter
3. Choose your venv

### PyCharm

1. Open `BalderFrameWork` as project
2. Set interpreter: Preferences → Project → Python Interpreter
3. Select venv

## Verification Checklist

After installation, verify everything works:

- ✅ Python version 3.8+
- ✅ All dependencies installed
- ✅ Configuration files present
- ✅ `python orchestrator/main.py --help` works
- ✅ Output and workspace directories created
- ✅ Can run simple project

```bash
# Quick test
python orchestrator/main.py \
  --task "Create a hello world React app" \
  --dry-run
```

## What's Next?

1. **[Quick Start](quickstart.md)** - Build your first project
2. **[First Project](first-project.md)** - Detailed walkthrough
3. **[Configuration](configuration.md)** - Customize settings
4. **[Examples](../examples/quick-examples.md)** - Real-world usage

## Need Help?

- 📚 **Documentation**: Browse [GitBook](https://byteclaude.gitbook.io)
- 💬 **Issues**: [GitHub Issues](https://github.com/bastdumont/BalderFrameWork/issues)
- 🤝 **Contributing**: [Contributing Guide](../development/contributing.md)

---

**Ready to build?** See [Quick Start](quickstart.md) for your first project.

