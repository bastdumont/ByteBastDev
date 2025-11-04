#!/usr/bin/env python3
"""
Setup Script for Automated Development Framework
Initializes the framework and verifies dependencies
"""

import sys
import subprocess
import os
from pathlib import Path
import yaml


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    directories = [
        "workspace",
        "output",
        "logs",
        "temp",
        "checkpoints"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"✓ Created {directory}/")
    
    return True


def verify_config_files():
    """Verify configuration files exist"""
    print("\nVerifying configuration files...")
    
    config_files = {
        "config/framework-config.yaml": "Main configuration",
        "config/mcp-registry.yaml": "MCP registry",
        "config/skills-manifest.yaml": "Skills manifest"
    }
    
    all_exist = True
    for file_path, description in config_files.items():
        if Path(file_path).exists():
            print(f"✓ {description}: {file_path}")
        else:
            print(f"❌ Missing {description}: {file_path}")
            all_exist = False
    
    return all_exist


def check_skills_directory():
    """Check if skills directory is accessible"""
    print("\nChecking skills directory...")
    skills_path = Path("/mnt/skills")
    
    if skills_path.exists():
        public_skills = list(skills_path.glob("public/*/SKILL.md"))
        example_skills = list(skills_path.glob("examples/*/SKILL.md"))
        
        print(f"✓ Skills directory found")
        print(f"  - Public skills: {len(public_skills)}")
        print(f"  - Example skills: {len(example_skills)}")
        return True
    else:
        print("⚠️  Warning: Skills directory not found at /mnt/skills")
        print("   Skills may not be available")
        return False


def check_mcps():
    """Check MCP availability"""
    print("\nChecking MCP availability...")
    
    # Try to load MCP registry
    try:
        with open("config/mcp-registry.yaml", "r") as f:
            registry = yaml.safe_load(f)
        
        mcps = registry.get("mcps", {})
        print(f"✓ Found {len(mcps)} registered MCPs:")
        
        # Show categories
        categories = {}
        for mcp_name, mcp_info in mcps.items():
            category = mcp_info.get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(mcp_name)
        
        for category, mcp_list in sorted(categories.items()):
            print(f"  - {category}: {', '.join(mcp_list)}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading MCP registry: {e}")
        return False


def verify_framework():
    """Verify framework can be imported"""
    print("\nVerifying framework modules...")
    
    try:
        sys.path.insert(0, str(Path("orchestrator")))
        from task_planner import TaskPlanner
        from execution_engine import ExecutionEngine
        print("✓ Core modules can be imported")
        return True
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        return False


def run_test_plan():
    """Run a test plan creation"""
    print("\nTesting plan creation...")
    
    try:
        sys.path.insert(0, str(Path("orchestrator")))
        from task_planner import TaskPlanner
        
        planner = TaskPlanner()
        plan = planner.create_execution_plan("Create a simple test project")
        
        print(f"✓ Test plan created successfully")
        print(f"  - Project: {plan.project_name}")
        print(f"  - Tasks: {len(plan.tasks)}")
        return True
    except Exception as e:
        print(f"❌ Test plan creation failed: {e}")
        return False


def print_summary(results):
    """Print setup summary"""
    print_header("SETUP SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    
    print(f"Checks performed: {total_checks}")
    print(f"Checks passed: {passed_checks}")
    print(f"Checks failed: {total_checks - passed_checks}\n")
    
    for check_name, passed in results.items():
        status = "✓" if passed else "❌"
        print(f"{status} {check_name}")
    
    print()
    
    if passed_checks == total_checks:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Read QUICKSTART.md for usage instructions")
        print("2. Try: python orchestrator/main.py --help")
        print("3. Start building: python orchestrator/main.py")
        return True
    else:
        print("⚠️  Setup completed with warnings")
        print("\nSome checks failed. The framework may still work,")
        print("but some features might not be available.")
        return False


def main():
    """Main setup function"""
    print_header("Automated Development Framework Setup")
    
    print("This script will:")
    print("1. Verify Python version")
    print("2. Install dependencies")
    print("3. Create necessary directories")
    print("4. Verify configuration")
    print("5. Check skills and MCPs")
    print("6. Test framework initialization")
    
    input("\nPress Enter to continue...")
    
    # Run all checks
    results = {}
    
    results["Python Version"] = check_python_version()
    if not results["Python Version"]:
        print("\n❌ Setup failed: Python version requirement not met")
        sys.exit(1)
    
    results["Dependencies"] = install_dependencies()
    results["Directories"] = create_directories()
    results["Configuration Files"] = verify_config_files()
    results["Skills Directory"] = check_skills_directory()
    results["MCP Registry"] = check_mcps()
    results["Framework Modules"] = verify_framework()
    results["Test Plan Creation"] = run_test_plan()
    
    # Print summary
    success = print_summary(results)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Exiting...")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
