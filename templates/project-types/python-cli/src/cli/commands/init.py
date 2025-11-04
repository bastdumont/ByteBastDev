import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from pathlib import Path
import yaml

console = Console()


@click.command()
@click.option(
    "--name",
    "-n",
    help="Project name",
)
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=".",
    help="Project directory path",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force initialization (overwrite existing)",
)
@click.pass_context
def init(ctx, name, path, force):
    """Initialize a new project"""
    console.print("[bold blue]Initializing new project...[/bold blue]\n")

    # Interactive prompts if not provided
    if not name:
        name = Prompt.ask("Project name", default="my-project")

    project_path = Path(path)
    config_file = project_path / ".{{command_name}}.yaml"

    # Check if already initialized
    if config_file.exists() and not force:
        if not Confirm.ask(
            f"Configuration file already exists at {config_file}. Overwrite?"
        ):
            console.print("[yellow]Initialization cancelled[/yellow]")
            return

    # Create configuration
    config = {
        "project": {
            "name": name,
            "version": "0.1.0",
            "created": "auto-generated",
        },
        "settings": {
            "verbose": False,
            "log_level": "INFO",
        },
    }

    # Write configuration file
    try:
        with open(config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        console.print(f"[green]✓[/green] Created configuration file: {config_file}")
        console.print(f"[green]✓[/green] Project '{name}' initialized successfully!")
        console.print(
            f"\n[dim]Next steps:[/dim]\n"
            f"  1. Edit {config_file} to customize your project\n"
            f"  2. Run '{{command_name}} run' to execute your project\n"
        )

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {str(e)}")
        raise click.Abort()
