#!/usr/bin/env python3
"""
Main CLI for Automated Development Framework
Entry point for natural language software development
"""

import sys
import argparse
import asyncio
import yaml
from pathlib import Path
from typing import Optional
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from task_planner import TaskPlanner
from execution_engine import ExecutionEngine


def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('framework.log')
        ]
    )


def load_config(config_path: Optional[str] = None) -> dict:
    """Load framework configuration"""
    default_config = {
        'framework': {
            'version': '1.0.0',
            'claude_code_enabled': True,
            'max_parallel_tasks': 5
        },
        'context7': {
            'enabled': True,
            'cache_documentation': True,
            'cache_ttl': 3600
        },
        'mcps': {
            'auto_discover': True
        },
        'skills': {
            'base_path': '/mnt/skills',
            'auto_load': True
        },
        'execution': {
            'work_directory': './workspace',
            'output_directory': './output',
            'log_level': 'INFO',
            'save_checkpoints': True
        },
        'validation': {
            'run_tests': True,
            'code_review': True,
            'generate_docs': True
        }
    }
    
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            # Merge configurations
            for key, value in user_config.items():
                if key in default_config and isinstance(value, dict):
                    default_config[key].update(value)
                else:
                    default_config[key] = value
    
    return default_config


def print_banner():
    """Print framework banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   Automated Microsoftware Development Framework                  ║
║   Claude Code + Skills + MCPs + Context7                        ║
║                                                                  ║
║   Powered by Claude Sonnet 4.5                                  ║
║   Version 1.0.0                                                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_plan_summary(plan):
    """Print execution plan summary"""
    print("\n" + "="*80)
    print("EXECUTION PLAN")
    print("="*80)
    print(f"Project: {plan.project_name}")
    print(f"Description: {plan.description}")
    print(f"Total Tasks: {len(plan.tasks)}")
    print(f"Estimated Duration: {plan.estimated_total_duration // 60} minutes")
    print("\nTasks:")
    
    for i, task_id in enumerate(plan.execution_order, 1):
        task = next(t for t in plan.tasks if t.id == task_id)
        print(f"  {i}. {task.name}")
        print(f"     Type: {task.task_type.value}")
        print(f"     Priority: {task.priority.name}")
        if task.requirements:
            reqs = ', '.join(f"{r.type}:{r.name}" for r in task.requirements)
            print(f"     Requirements: {reqs}")
    
    if 'parallel_groups' in plan.metadata:
        print(f"\nParallel Execution Groups: {len(plan.metadata['parallel_groups'])}")
        for i, group in enumerate(plan.metadata['parallel_groups'], 1):
            tasks = [next(t for t in plan.tasks if t.id == tid).name for tid in group]
            print(f"  Group {i}: {', '.join(tasks)}")
    
    print("="*80)


def print_execution_summary(results):
    """Print execution results summary"""
    total = len(results)
    completed = sum(1 for r in results.values() if r.status.value == 'completed')
    failed = sum(1 for r in results.values() if r.status.value == 'failed')
    skipped = sum(1 for r in results.values() if r.status.value == 'skipped')
    
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"Total Tasks: {total}")
    print(f"✓ Completed: {completed}")
    print(f"✗ Failed: {failed}")
    print(f"⊘ Skipped: {skipped}")
    print(f"Success Rate: {(completed/total*100):.1f}%")
    
    total_duration = sum(r.duration for r in results.values())
    print(f"Total Duration: {total_duration:.2f}s ({total_duration/60:.1f}m)")
    
    print("\nTask Results:")
    for task_id, result in results.items():
        status_symbol = {
            'completed': '✓',
            'failed': '✗',
            'skipped': '⊘',
            'pending': '○'
        }.get(result.status.value, '?')
        
        print(f"  {status_symbol} {task_id}: {result.status.value} ({result.duration:.2f}s)")
        if result.error:
            print(f"     Error: {result.error}")
    
    print("="*80)


async def run_interactive_mode(config):
    """Run framework in interactive mode"""
    print_banner()
    print("\nInteractive Mode - Enter 'exit' to quit\n")
    
    planner = TaskPlanner(config)
    engine = ExecutionEngine(config)
    
    while True:
        try:
            request = input("\n📝 Describe what you want to build: ").strip()
            
            if not request:
                continue
            
            if request.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            # Create plan
            print("\n🔄 Creating execution plan...")
            plan = planner.create_execution_plan(request)
            plan = planner.optimize_plan(plan)
            
            # Show plan
            print_plan_summary(plan)
            
            # Confirm execution
            confirm = input("\n▶️  Execute this plan? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Plan cancelled.")
                continue
            
            # Execute
            print("\n🚀 Starting execution...\n")
            results = await engine.execute_plan(plan)
            
            # Show results
            print_execution_summary(results)
            
            # Show output location
            print(f"\n📁 Output directory: {engine.context.output_directory}")
            print(f"📄 Execution report: {engine.context.output_directory}/execution_report.json")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            logging.exception("Error in interactive mode")


async def run_single_task(task_description: str, config: dict, output_dir: Optional[str] = None):
    """Run a single task from command line"""
    print_banner()
    
    # Override output directory if specified
    if output_dir:
        config['execution']['output_directory'] = output_dir
    
    planner = TaskPlanner(config)
    engine = ExecutionEngine(config)
    
    print(f"\n📝 Task: {task_description}\n")
    
    # Create plan
    print("🔄 Creating execution plan...")
    plan = planner.create_execution_plan(task_description)
    plan = planner.optimize_plan(plan)
    
    # Show plan
    print_plan_summary(plan)
    
    # Execute
    print("\n🚀 Starting execution...\n")
    results = await engine.execute_plan(plan)
    
    # Show results
    print_execution_summary(results)
    
    # Show output location
    print(f"\n📁 Output directory: {engine.context.output_directory}")
    print(f"📄 Execution report: {engine.context.output_directory}/execution_report.json")
    
    # Return success status
    completed = sum(1 for r in results.values() if r.status.value == 'completed')
    return completed == len(results)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Automated Microsoftware Development Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py
  
  # Single task
  python main.py --task "Create a React dashboard with MongoDB"
  
  # With output directory
  python main.py --task "Build a Next.js app" --output-dir ./my-app
  
  # Custom config
  python main.py --config ./my-config.yaml --task "Generate PDF reports"
  
  # With specific skills
  python main.py --task "Create docs" --use-skills docx,pdf
  
  # Include tests
  python main.py --task "Build API" --include-tests
  
  # Dry run (plan only)
  python main.py --task "Build app" --dry-run
        """
    )
    
    parser.add_argument(
        '--task', '-t',
        type=str,
        help='Task description in natural language'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        help='Output directory for generated files'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--use-skills',
        type=str,
        help='Comma-separated list of skills to use'
    )
    
    parser.add_argument(
        '--use-mcps',
        type=str,
        help='Comma-separated list of MCPs to use'
    )
    
    parser.add_argument(
        '--include-tests',
        action='store_true',
        help='Include test generation'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show plan without executing'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Automated Dev Framework v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Update config with CLI args
    if args.include_tests:
        config['validation']['run_tests'] = True
    
    # Run appropriate mode
    try:
        if args.interactive or (not args.task and not args.dry_run):
            # Interactive mode
            asyncio.run(run_interactive_mode(config))
        elif args.task:
            if args.dry_run:
                # Dry run - show plan only
                print_banner()
                planner = TaskPlanner(config)
                plan = planner.create_execution_plan(args.task)
                plan = planner.optimize_plan(plan)
                print_plan_summary(plan)
                print("\n⚠️  Dry run - no execution performed")
            else:
                # Execute single task
                success = asyncio.run(run_single_task(args.task, config, args.output_dir))
                sys.exit(0 if success else 1)
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        logging.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
