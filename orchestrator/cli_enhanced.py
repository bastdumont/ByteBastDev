"""
Enhanced CLI with Rich UI Components
Provides beautiful terminal interface for ByteClaude
"""

from typing import List, Optional, Any, Callable
from enum import Enum
import sys

# Try importing rich, fall back to basic if not available
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.tree import Tree
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None


class UILevel(Enum):
    """UI output level"""
    MINIMAL = "minimal"
    NORMAL = "normal"
    VERBOSE = "verbose"


class EnhancedCLI:
    """
    Enhanced CLI interface with rich formatting and interactive features
    """

    def __init__(self, level: UILevel = UILevel.NORMAL):
        self.level = level
        self.console = Console() if RICH_AVAILABLE else None
        self.command_history: List[str] = []

    def print_welcome(self):
        """Print welcome banner"""
        if not RICH_AVAILABLE:
            print("=" * 60)
            print("ByteClaude Automated Development Framework")
            print("=" * 60)
            return

        banner = """
        [bold cyan]╔╗╔╗ ╔═╗╔╦╗╔═╗╔═╗╦  ╔═╗╦ ╦╔╦╗╔═╗[/bold cyan]
        [bold cyan]║║║║ ╚═╗║║║║╔╝║  ║  ╠═╣║║║║║║║╣ [/bold cyan]
        [bold cyan]╝╚╝╚╗╚═╝╩ ╩╩╚╝╚═╝╩═╝╩ ╩╚═╝╩ ╩╚═╝[/bold cyan]
        
        [bold]Automated Development Framework[/bold]
        [dim]Powered by Claude + Skills + MCPs + Context7[/dim]
        """

        self.console.print(banner)

    def print_section(self, title: str, content: str = ""):
        """Print a section with title"""
        if not RICH_AVAILABLE:
            print(f"\n{'='*60}")
            print(f"{title}")
            print(f"{'='*60}")
            if content:
                print(content)
            return

        panel = Panel(
            Markdown(content) if content else "",
            title=f"[bold]{title}[/bold]",
            border_style="cyan",
            expand=True
        )
        self.console.print(panel)

    def print_task_progress(self, tasks: List[str], current: int):
        """Print task progress"""
        if not RICH_AVAILABLE:
            print(f"Progress: {current}/{len(tasks)} tasks")
            return

        tree = Tree(f"[bold]Tasks ({current}/{len(tasks)})[/bold]")
        
        for i, task in enumerate(tasks):
            if i < current:
                tree.add(f"[green]✓[/green] {task}")
            elif i == current:
                tree.add(f"[yellow]→[/yellow] {task}")
            else:
                tree.add(f"[dim]○[/dim] {task}")

        self.console.print(tree)

    def print_table(
        self,
        data: List[List[Any]],
        headers: List[str],
        title: str = ""
    ):
        """Print a formatted table"""
        if not RICH_AVAILABLE:
            print(f"\n{title}")
            print("-" * 60)
            for row in data:
                print(" | ".join(str(cell) for cell in row))
            return

        table = Table(title=title)
        
        for header in headers:
            table.add_column(header)
        
        for row in data:
            table.add_row(*[str(cell) for cell in row])

        self.console.print(table)

    def print_code(self, code: str, language: str = "python", title: str = ""):
        """Print formatted code"""
        if not RICH_AVAILABLE:
            print(f"\n{title}")
            print(code)
            return

        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        if title:
            panel = Panel(syntax, title=title, expand=True)
            self.console.print(panel)
        else:
            self.console.print(syntax)

    def print_error(self, message: str):
        """Print error message"""
        if not RICH_AVAILABLE:
            print(f"ERROR: {message}", file=sys.stderr)
            return

        self.console.print(f"[bold red]✗ ERROR[/bold red]: {message}")

    def print_success(self, message: str):
        """Print success message"""
        if not RICH_AVAILABLE:
            print(f"✓ {message}")
            return

        self.console.print(f"[bold green]✓ SUCCESS[/bold green]: {message}")

    def print_warning(self, message: str):
        """Print warning message"""
        if not RICH_AVAILABLE:
            print(f"⚠ WARNING: {message}")
            return

        self.console.print(f"[bold yellow]⚠ WARNING[/bold yellow]: {message}")

    def print_info(self, message: str):
        """Print info message"""
        if not RICH_AVAILABLE:
            print(f"ℹ {message}")
            return

        self.console.print(f"[bold blue]ℹ INFO[/bold blue]: {message}")

    def prompt_input(self, prompt: str, default: str = "") -> str:
        """Get user input with prompt"""
        if not RICH_AVAILABLE:
            return input(prompt + (f" [{default}]" if default else "") + ": ")

        return Prompt.ask(prompt, default=default)

    def prompt_confirm(self, prompt: str, default: bool = True) -> bool:
        """Get yes/no confirmation"""
        if not RICH_AVAILABLE:
            response = input(prompt + " [Y/n]: " if default else " [y/N]: ")
            if default:
                return response.lower() != "n"
            else:
                return response.lower() == "y"

        return Confirm.ask(prompt, default=default)

    def show_progress(self, description: str, total: int) -> Any:
        """Show progress bar"""
        if not RICH_AVAILABLE or not self.console:
            class SimpleProgress:
                def __init__(self, desc, tot):
                    self.count = 0
                    self.total = tot
                    self.desc = desc
                
                def update(self, inc=1):
                    self.count += inc
                    print(f"{self.desc}: {self.count}/{self.total}")
            
            return SimpleProgress(description, total)

        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        )
        
        return progress.start_task(description, total=total)

    def print_workflow(self, workflow_data: dict):
        """Print workflow in tree format"""
        if not RICH_AVAILABLE:
            print("Workflow:")
            print(str(workflow_data))
            return

        tree = Tree("[bold]Workflow[/bold]")
        
        for node_id, node_data in workflow_data.get("nodes", {}).items():
            node_tree = tree.add(f"[cyan]{node_id}[/cyan]: {node_data.get('title', '')}")
            if node_data.get('description'):
                node_tree.add(f"[dim]{node_data['description']}[/dim]")

        self.console.print(tree)

    def interactive_menu(
        self,
        title: str,
        options: List[str],
        prompt: str = "Choose an option"
    ) -> int:
        """Show interactive menu"""
        if not RICH_AVAILABLE:
            print(f"\n{title}")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            while True:
                try:
                    choice = int(input(prompt + ": ")) - 1
                    if 0 <= choice < len(options):
                        return choice
                except ValueError:
                    pass
            return 0

        from rich.prompt import IntPrompt
        
        self.print_section(title)
        for i, option in enumerate(options, 1):
            self.console.print(f"  [cyan]{i}[/cyan]. {option}")

        return IntPrompt.ask(prompt, console=self.console) - 1

    def save_command(self, command: str):
        """Save command to history"""
        self.command_history.append(command)

    def show_help(self, command_help: dict):
        """Show help information"""
        if not RICH_AVAILABLE:
            print("Available Commands:")
            for cmd, desc in command_help.items():
                print(f"  {cmd}: {desc}")
            return

        help_text = "\n".join(
            f"[cyan]{cmd}[/cyan]: {desc}"
            for cmd, desc in command_help.items()
        )
        
        self.print_section("Available Commands", help_text)


# Helper function to create CLI instance
def create_cli(level: UILevel = UILevel.NORMAL) -> EnhancedCLI:
    """Create enhanced CLI instance"""
    return EnhancedCLI(level)


# Example usage
if __name__ == "__main__":
    cli = create_cli(UILevel.VERBOSE)
    cli.print_welcome()
    cli.print_section("Getting Started", "Welcome to ByteClaude!")
    cli.print_success("CLI initialized successfully")
    cli.print_table(
        [["Python", "3.11"], ["Status", "Ready"]],
        ["Component", "Version"],
        "System Information"
    )
