# {{project_name}} - Python CLI Tool

A production-ready Python CLI tool built with Click, Rich, and modern best practices.

## Features

- ✅ **Click** for command-line interface
- ✅ **Rich** for beautiful terminal output
- ✅ **Pydantic** for configuration management
- ✅ **YAML/JSON** configuration support
- ✅ **Environment variables** support
- ✅ **Subcommands** and command groups
- ✅ **Input validation**
- ✅ **Logging** with file and console output
- ✅ **Testing** with pytest
- ✅ **Type hints** throughout
- ✅ **Package distribution** ready

## Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd {{project_name}}

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Display help
{{command_name}} --help

# Initialize a project
{{command_name}} init --name my-project

# Run with configuration
{{command_name}} --config config.yaml run

# Enable verbose output
{{command_name}} -v hello

# Display information
{{command_name}} info
```

## Project Structure

```
{{project_name}}/
├── src/
│   ├── cli/                   # CLI commands
│   │   ├── main.py           # Main CLI entry point
│   │   └── commands/         # Command modules
│   │       ├── init.py       # Initialize command
│   │       ├── run.py        # Run command
│   │       └── config.py     # Config command
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration management
│   │   └── processor.py      # Business logic
│   └── utils/                # Utilities
│       ├── logger.py         # Logging setup
│       └── validators.py     # Validation functions
├── tests/                    # Test suite
│   ├── test_cli.py
│   ├── test_config.py
│   └── conftest.py
├── setup.py                  # Package configuration
├── README.md                 # This file
├── pyproject.toml           # Build configuration
└── .{{command_name}}.yaml   # Default configuration
```

## Available Commands

### `init`

Initialize a new project with configuration:

```bash
{{command_name}} init --name my-project --path ./projects
```

Options:
- `--name, -n`: Project name
- `--path, -p`: Project directory (default: current directory)
- `--force, -f`: Force overwrite existing configuration

### `run`

Execute the main functionality:

```bash
{{command_name}} run --input data.txt --output results.txt
```

Options:
- `--input, -i`: Input file path
- `--output, -o`: Output file path
- `--batch, -b`: Batch processing mode

### `config`

Manage configuration:

```bash
# Show current configuration
{{command_name}} config show

# Set a configuration value
{{command_name}} config set key value

# Get a configuration value
{{command_name}} config get key

# Validate configuration
{{command_name}} config validate
```

### `info`

Display CLI tool information:

```bash
{{command_name}} info
```

## Configuration

### Configuration File

Create a `.{{command_name}}.yaml` file in your project directory:

```yaml
project:
  name: my-project
  version: 0.1.0

settings:
  verbose: false
  log_level: INFO
  output_format: json

custom:
  api_key: ${API_KEY}  # Environment variable
  timeout: 30
```

### Environment Variables

Configuration values can reference environment variables:

```yaml
api_key: ${API_KEY}
database_url: ${DATABASE_URL:-sqlite:///default.db}  # With default
```

Set environment variables:

```bash
export API_KEY="your-api-key"
export DATABASE_URL="postgresql://localhost/mydb"
```

### Command-line Options

Global options available for all commands:

```bash
{{command_name}} --config custom-config.yaml  # Custom config file
{{command_name}} --verbose                     # Verbose output
{{command_name}} --help                        # Show help
```

## Development

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_cli.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with Black
black src tests

# Lint with Ruff
ruff check src tests

# Type check with mypy
mypy src
```

### Adding New Commands

1. Create a new file in `src/cli/commands/`:

```python
# src/cli/commands/mycommand.py
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('--option', help='Command option')
@click.pass_context
def mycommand(ctx, option):
    """My new command description"""
    console.print(f"Executing mycommand with option: {option}")
```

2. Register in `src/cli/main.py`:

```python
from cli.commands import mycommand

cli.add_command(mycommand.mycommand)
```

## Building and Distribution

### Building Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# This creates:
# - dist/{{project_name}}-0.1.0-py3-none-any.whl
# - dist/{{project_name}}-0.1.0.tar.gz
```

### Publishing to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Installing from PyPI

```bash
pip install {{project_name}}
```

## Examples

### Example 1: Process Files

```bash
{{command_name}} run --input data.csv --output results.json
```

### Example 2: Batch Processing

```bash
{{command_name}} run --batch --input-dir ./data --output-dir ./results
```

### Example 3: With Custom Configuration

```bash
{{command_name}} --config production.yaml run --input data.txt
```

### Example 4: Interactive Mode

```bash
{{command_name}} init
# Follow interactive prompts
```

## Rich Terminal Output

The CLI uses Rich for enhanced terminal output:

- **Colored output**: Success (green), errors (red), warnings (yellow)
- **Tables**: Display data in formatted tables
- **Progress bars**: Show progress for long operations
- **Syntax highlighting**: For code and JSON output
- **Panels**: Group related information

Example output:

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Results")
table.add_column("Name")
table.add_column("Status")
table.add_row("Task 1", "[green]✓ Complete[/green]")
console.print(table)
```

## Logging

Logging is configured in `src/utils/logger.py`:

```python
import logging
from utils.logger import setup_logger

logger = setup_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

Logs are written to:
- Console (colored output)
- File: `{{project_name}}.log`

## Error Handling

The CLI includes comprehensive error handling:

```python
try:
    # Your code
    result = process_data(input_file)
except FileNotFoundError:
    console.print("[red]Error: File not found[/red]")
    raise click.Abort()
except Exception as e:
    logger.exception("Unexpected error")
    console.print(f"[red]Error: {str(e)}[/red]")
    raise
```

## Best Practices

1. **Use type hints**: Add type annotations to all functions
2. **Document commands**: Add docstrings to all Click commands
3. **Validate input**: Use Pydantic for configuration validation
4. **Handle errors**: Provide helpful error messages
5. **Test thoroughly**: Write tests for all commands
6. **Log appropriately**: Use appropriate log levels
7. **Configuration**: Support both files and environment variables

## Troubleshooting

### Command not found

If `{{command_name}}` is not found after installation:

```bash
# Reinstall in editable mode
pip install -e .

# Or check if it's in PATH
which {{command_name}}
```

### Import errors

```bash
# Ensure package is installed
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

### Configuration not loading

```bash
# Verify configuration file exists
ls -la .{{command_name}}.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.{{command_name}}.yaml'))"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linters
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Resources

- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Packaging Guide](https://packaging.python.org/)
