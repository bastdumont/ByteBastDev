import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

from cli.commands import init, run, config
from core.config import load_config, get_config
from utils.logger import setup_logger

console = Console()
logger = setup_logger(__name__)


@click.group()
@click.version_option(version="0.1.0")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.pass_context
def cli(ctx, config, verbose):
    """
    {{project_name}} - A production-ready Python CLI tool

    Use --help with any command for more information.
    """
    ctx.ensure_object(dict)

    # Load configuration
    if config:
        ctx.obj["config"] = load_config(Path(config))
    else:
        ctx.obj["config"] = get_config()

    # Set verbosity
    ctx.obj["verbose"] = verbose

    if verbose:
        logger.setLevel("DEBUG")
        console.print("[yellow]Verbose mode enabled[/yellow]")


# Register command groups
cli.add_command(init.init)
cli.add_command(run.run)
cli.add_command(config.config)


@cli.command()
@click.pass_context
def info(ctx):
    """Display information about the CLI tool"""
    table = Table(title="{{project_name}} Information")

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", "0.1.0")
    table.add_row("Python Version", "3.11+")
    table.add_row("Config Loaded", str(ctx.obj.get("config") is not None))
    table.add_row("Verbose Mode", str(ctx.obj.get("verbose", False)))

    console.print(table)


@cli.command()
def hello():
    """Say hello (example command)"""
    console.print("[bold green]Hello from {{project_name}}![/bold green]")
    console.print("This is a production-ready CLI tool template.")


if __name__ == "__main__":
    cli()
