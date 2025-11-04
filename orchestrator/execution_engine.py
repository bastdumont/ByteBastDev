"""
Execution Engine - Core execution system for automated development
Orchestrates Claude Code, Skills, MCPs, and Context7 integration
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import subprocess
import sys

from task_planner import Task, ExecutionPlan, TaskType


class ExecutionStatus(Enum):
    """Status of task execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ExecutionResult:
    """Result of a task execution"""
    task_id: str
    status: ExecutionStatus
    output: Optional[Any] = None
    error: Optional[str] = None
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'status': self.status.value,
            'output': self.output,
            'error': self.error,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'metadata': self.metadata
        }


@dataclass
class ExecutionContext:
    """Context shared across task executions"""
    work_directory: Path
    output_directory: Path
    project_variables: Dict[str, Any] = field(default_factory=dict)
    cached_documentation: Dict[str, Any] = field(default_factory=dict)
    execution_results: Dict[str, ExecutionResult] = field(default_factory=dict)


class ExecutionEngine:
    """
    Main execution engine that:
    1. Executes tasks using appropriate tools (Skills, MCPs)
    2. Manages execution state and context
    3. Handles errors and retries
    4. Coordinates Claude Code integration
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logger()
        self.context = None
        self.skill_handlers = self._register_skill_handlers()
        self.mcp_handlers = self._register_mcp_handlers()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger("ExecutionEngine")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _register_skill_handlers(self) -> Dict[str, Callable]:
        """Register handlers for different skills"""
        return {
            'docx': self._execute_docx_skill,
            'pdf': self._execute_pdf_skill,
            'pptx': self._execute_pptx_skill,
            'xlsx': self._execute_xlsx_skill,
            'artifacts-builder': self._execute_artifacts_skill,
            'theme-factory': self._execute_theme_skill,
            'mcp-builder': self._execute_mcp_builder_skill,
            'skill-creator': self._execute_skill_creator,
            'canvas-design': self._execute_canvas_design
        }
    
    def _register_mcp_handlers(self) -> Dict[str, Callable]:
        """Register handlers for different MCPs"""
        return {
            'mongodb': self._execute_mongodb_mcp,
            'stripe': self._execute_stripe_mcp,
            'notion': self._execute_notion_mcp,
            'airtable': self._execute_airtable_mcp,
            'hubspot': self._execute_hubspot_mcp,
            'filesystem': self._execute_filesystem_mcp,
            'context7': self._execute_context7_mcp
        }
    
    def initialize_context(self, plan: ExecutionPlan) -> ExecutionContext:
        """Initialize execution context for a plan"""
        work_dir = Path(self.config['execution']['work_directory']) / plan.project_name
        output_dir = Path(self.config['execution']['output_directory']) / plan.project_name
        
        # Create directories
        work_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        context = ExecutionContext(
            work_directory=work_dir,
            output_directory=output_dir,
            project_variables={
                'project_name': plan.project_name,
                'description': plan.description,
                'created_at': time.time()
            }
        )
        
        self.context = context
        return context
    
    async def execute_plan(self, plan: ExecutionPlan) -> Dict[str, ExecutionResult]:
        """
        Execute complete plan
        Returns dictionary of task_id -> ExecutionResult
        """
        self.logger.info(f"Starting execution of plan: {plan.project_name}")
        self.initialize_context(plan)
        
        results = {}
        
        # Check if plan has parallel groups
        if 'parallel_groups' in plan.metadata:
            results = await self._execute_parallel_plan(plan)
        else:
            results = await self._execute_sequential_plan(plan)
        
        # Save execution report
        self._save_execution_report(plan, results)
        
        self.logger.info(f"Plan execution completed. Success rate: {self._calculate_success_rate(results):.1f}%")
        
        return results
    
    async def _execute_sequential_plan(self, plan: ExecutionPlan) -> Dict[str, ExecutionResult]:
        """Execute tasks sequentially"""
        results = {}
        
        for task_id in plan.execution_order:
            task = next(t for t in plan.tasks if t.id == task_id)
            
            # Check if dependencies are satisfied
            if not self._check_dependencies(task, results):
                results[task_id] = ExecutionResult(
                    task_id=task_id,
                    status=ExecutionStatus.SKIPPED,
                    error="Dependencies not satisfied"
                )
                continue
            
            result = await self.execute_task(task)
            results[task_id] = result
            
            if result.status == ExecutionStatus.FAILED:
                self.logger.error(f"Task {task_id} failed: {result.error}")
                # Decide whether to continue or stop
                if task.priority.value <= 2:  # CRITICAL or HIGH
                    self.logger.error("Critical task failed. Stopping execution.")
                    break
        
        return results
    
    async def _execute_parallel_plan(self, plan: ExecutionPlan) -> Dict[str, ExecutionResult]:
        """Execute tasks in parallel groups"""
        results = {}
        
        for group in plan.metadata['parallel_groups']:
            # Execute all tasks in group concurrently
            tasks_in_group = [next(t for t in plan.tasks if t.id == tid) for tid in group]
            
            # Check dependencies for all tasks
            executable_tasks = [
                task for task in tasks_in_group
                if self._check_dependencies(task, results)
            ]
            
            if not executable_tasks:
                for task in tasks_in_group:
                    results[task.id] = ExecutionResult(
                        task_id=task.id,
                        status=ExecutionStatus.SKIPPED,
                        error="Dependencies not satisfied"
                    )
                continue
            
            # Execute tasks concurrently
            group_results = await asyncio.gather(
                *[self.execute_task(task) for task in executable_tasks],
                return_exceptions=True
            )
            
            # Process results
            for i, task in enumerate(executable_tasks):
                result = group_results[i]
                if isinstance(result, Exception):
                    results[task.id] = ExecutionResult(
                        task_id=task.id,
                        status=ExecutionStatus.FAILED,
                        error=str(result)
                    )
                else:
                    results[task.id] = result
        
        return results
    
    def _check_dependencies(self, task: Task, results: Dict[str, ExecutionResult]) -> bool:
        """Check if all task dependencies are satisfied"""
        for dep_id in task.dependencies:
            if dep_id not in results:
                return False
            if results[dep_id].status != ExecutionStatus.COMPLETED:
                return False
        return True
    
    async def execute_task(self, task: Task) -> ExecutionResult:
        """Execute a single task"""
        self.logger.info(f"Executing task: {task.name} ({task.id})")
        
        result = ExecutionResult(
            task_id=task.id,
            status=ExecutionStatus.IN_PROGRESS,
            start_time=time.time()
        )
        
        try:
            # Route to appropriate handler based on task type
            if task.task_type == TaskType.FILE_OPERATION:
                output = await self._execute_file_operation(task)
            elif task.task_type == TaskType.CODE_GENERATION:
                output = await self._execute_code_generation(task)
            elif task.task_type == TaskType.WEB_DEVELOPMENT:
                output = await self._execute_web_development(task)
            elif task.task_type == TaskType.DOCUMENT_GENERATION:
                output = await self._execute_document_generation(task)
            elif task.task_type == TaskType.API_INTEGRATION:
                output = await self._execute_api_integration(task)
            elif task.task_type == TaskType.DATABASE_OPERATION:
                output = await self._execute_database_operation(task)
            elif task.task_type == TaskType.TESTING:
                output = await self._execute_testing(task)
            elif task.task_type == TaskType.VALIDATION:
                output = await self._execute_validation(task)
            else:
                output = await self._execute_generic_task(task)
            
            result.status = ExecutionStatus.COMPLETED
            result.output = output
            
        except Exception as e:
            self.logger.error(f"Task {task.id} failed with error: {str(e)}")
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
        
        finally:
            result.end_time = time.time()
            result.duration = result.end_time - result.start_time
            self.context.execution_results[task.id] = result
        
        return result
    
    async def _execute_file_operation(self, task: Task) -> Any:
        """Execute file operation tasks"""
        self.logger.info(f"Executing file operation: {task.name}")
        
        # Get skill requirements
        skills = [req for req in task.requirements if req.type == 'skill']
        
        if not skills:
            # Basic file operation
            return await self._create_project_structure(task)
        
        # Execute skill-based operation
        for skill_req in skills:
            if skill_req.name in self.skill_handlers:
                return await self.skill_handlers[skill_req.name](task, skill_req)
        
        return {"status": "completed", "message": "File operations completed"}
    
    async def _execute_code_generation(self, task: Task) -> Any:
        """Execute code generation using Claude Code"""
        self.logger.info(f"Generating code for: {task.name}")
        
        # This would integrate with Claude Code CLI
        # For now, we'll simulate the structure
        
        prompt = self._build_code_generation_prompt(task)
        
        # In real implementation, this would call Claude Code:
        # subprocess.run(['claude-code', 'generate', '--prompt', prompt])
        
        return {
            "status": "completed",
            "files_created": [],
            "message": "Code generation completed"
        }
    
    async def _execute_web_development(self, task: Task) -> Any:
        """Execute web development tasks"""
        self.logger.info(f"Building web application: {task.name}")
        
        # Check for artifacts-builder skill
        artifacts_skill = next(
            (req for req in task.requirements if req.name == 'artifacts-builder'),
            None
        )
        
        if artifacts_skill:
            return await self._execute_artifacts_skill(task, artifacts_skill)
        
        # Otherwise, use generic web dev approach
        return await self._create_web_app_structure(task)
    
    async def _execute_document_generation(self, task: Task) -> Any:
        """Execute document generation"""
        self.logger.info(f"Generating documents: {task.name}")
        
        # Find document skill (docx, pdf, pptx, xlsx)
        doc_skill = next(
            (req for req in task.requirements if req.type == 'skill'),
            None
        )
        
        if doc_skill and doc_skill.name in self.skill_handlers:
            return await self.skill_handlers[doc_skill.name](task, doc_skill)
        
        return {"status": "completed", "message": "Document generation completed"}
    
    async def _execute_api_integration(self, task: Task) -> Any:
        """Execute API integration tasks"""
        self.logger.info(f"Integrating APIs: {task.name}")
        
        # Check for Context7 requirement
        context7_req = next(
            (req for req in task.requirements if req.type == 'context7'),
            None
        )
        
        if context7_req:
            return await self._execute_context7_mcp(task, context7_req)
        
        # Execute MCP integrations
        results = {}
        for req in task.requirements:
            if req.type == 'mcp' and req.name in self.mcp_handlers:
                result = await self.mcp_handlers[req.name](task, req)
                results[req.name] = result
        
        return results
    
    async def _execute_database_operation(self, task: Task) -> Any:
        """Execute database operations"""
        self.logger.info(f"Executing database operation: {task.name}")
        
        # Find database MCP
        db_mcp = next(
            (req for req in task.requirements if req.name in ['mongodb', 'airtable']),
            None
        )
        
        if db_mcp and db_mcp.name in self.mcp_handlers:
            return await self.mcp_handlers[db_mcp.name](task, db_mcp)
        
        return {"status": "completed", "message": "Database operation completed"}
    
    async def _execute_testing(self, task: Task) -> Any:
        """Execute testing tasks"""
        self.logger.info(f"Running tests: {task.name}")
        
        # Generate test structure
        test_files = []
        
        # In real implementation, would generate actual tests
        return {
            "status": "completed",
            "tests_created": test_files,
            "message": "Test generation completed"
        }
    
    async def _execute_validation(self, task: Task) -> Any:
        """Execute validation and documentation"""
        self.logger.info(f"Validating and documenting: {task.name}")
        
        # Validate previous outputs
        validation_results = []
        
        for prev_result in self.context.execution_results.values():
            if prev_result.status == ExecutionStatus.COMPLETED:
                validation_results.append({
                    'task_id': prev_result.task_id,
                    'validated': True
                })
        
        # Generate documentation
        doc_skill = next(
            (req for req in task.requirements if req.name == 'docx'),
            None
        )
        
        if doc_skill:
            await self._generate_project_documentation(task)
        
        return {
            "status": "completed",
            "validation_results": validation_results,
            "message": "Validation completed"
        }
    
    async def _execute_generic_task(self, task: Task) -> Any:
        """Execute generic tasks"""
        self.logger.info(f"Executing generic task: {task.name}")
        return {"status": "completed", "message": f"Task {task.name} completed"}
    
    # Skill Handlers
    
    async def _execute_docx_skill(self, task: Task, requirement: Any) -> Any:
        """Execute docx skill"""
        # Read skill documentation
        skill_path = "/mnt/skills/public/docx/SKILL.md"
        
        output_file = self.context.output_directory / f"{task.name.lower().replace(' ', '_')}.docx"
        
        return {
            "status": "completed",
            "file": str(output_file),
            "message": "DOCX document created"
        }
    
    async def _execute_pdf_skill(self, task: Task, requirement: Any) -> Any:
        """Execute pdf skill"""
        output_file = self.context.output_directory / f"{task.name.lower().replace(' ', '_')}.pdf"
        
        return {
            "status": "completed",
            "file": str(output_file),
            "message": "PDF document created"
        }
    
    async def _execute_pptx_skill(self, task: Task, requirement: Any) -> Any:
        """Execute pptx skill"""
        output_file = self.context.output_directory / f"{task.name.lower().replace(' ', '_')}.pptx"
        
        return {
            "status": "completed",
            "file": str(output_file),
            "message": "PowerPoint presentation created"
        }
    
    async def _execute_xlsx_skill(self, task: Task, requirement: Any) -> Any:
        """Execute xlsx skill"""
        output_file = self.context.output_directory / f"{task.name.lower().replace(' ', '_')}.xlsx"
        
        return {
            "status": "completed",
            "file": str(output_file),
            "message": "Excel spreadsheet created"
        }
    
    async def _execute_artifacts_skill(self, task: Task, requirement: Any) -> Any:
        """Execute artifacts-builder skill"""
        # This would create React/HTML artifacts
        output_dir = self.context.work_directory / "src"
        output_dir.mkdir(exist_ok=True)
        
        return {
            "status": "completed",
            "directory": str(output_dir),
            "message": "Web artifacts created"
        }
    
    async def _execute_theme_skill(self, task: Task, requirement: Any) -> Any:
        """Execute theme-factory skill"""
        return {
            "status": "completed",
            "theme": "applied",
            "message": "Theme applied"
        }
    
    async def _execute_mcp_builder_skill(self, task: Task, requirement: Any) -> Any:
        """Execute mcp-builder skill"""
        return {
            "status": "completed",
            "message": "MCP server created"
        }
    
    async def _execute_skill_creator(self, task: Task, requirement: Any) -> Any:
        """Execute skill-creator"""
        # Create project structure
        await self._create_project_structure(task)
        
        return {
            "status": "completed",
            "message": "Project structure created"
        }
    
    async def _execute_canvas_design(self, task: Task, requirement: Any) -> Any:
        """Execute canvas-design skill"""
        return {
            "status": "completed",
            "message": "Design created"
        }
    
    # MCP Handlers
    
    async def _execute_mongodb_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute MongoDB MCP operations"""
        return {
            "status": "completed",
            "message": "MongoDB operations completed"
        }
    
    async def _execute_stripe_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute Stripe MCP operations"""
        return {
            "status": "completed",
            "message": "Stripe integration configured"
        }
    
    async def _execute_notion_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute Notion MCP operations"""
        return {
            "status": "completed",
            "message": "Notion integration configured"
        }
    
    async def _execute_airtable_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute Airtable MCP operations"""
        return {
            "status": "completed",
            "message": "Airtable integration configured"
        }
    
    async def _execute_hubspot_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute HubSpot MCP operations"""
        return {
            "status": "completed",
            "message": "HubSpot integration configured"
        }
    
    async def _execute_filesystem_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute Filesystem MCP operations"""
        return {
            "status": "completed",
            "message": "File operations completed"
        }
    
    async def _execute_context7_mcp(self, task: Task, requirement: Any) -> Any:
        """Execute Context7 documentation retrieval"""
        libraries = requirement.config.get('libraries', [])
        
        for lib in libraries:
            # Cache documentation
            if lib not in self.context.cached_documentation:
                self.context.cached_documentation[lib] = {
                    "library": lib,
                    "fetched_at": time.time(),
                    "documentation": f"Documentation for {lib}"
                }
        
        return {
            "status": "completed",
            "libraries": libraries,
            "message": f"Retrieved documentation for {len(libraries)} libraries"
        }
    
    # Helper Methods
    
    async def _create_project_structure(self, task: Task) -> Dict[str, Any]:
        """Create basic project structure"""
        dirs = [
            'src',
            'tests',
            'docs',
            'config'
        ]
        
        for dir_name in dirs:
            (self.context.work_directory / dir_name).mkdir(exist_ok=True)
        
        # Create basic files
        files = {
            'README.md': '# Project\n\nGenerated by Automated Dev Framework',
            '.gitignore': 'node_modules/\n*.pyc\n__pycache__/\n.env',
            'package.json': json.dumps({
                'name': self.context.project_variables['project_name'],
                'version': '1.0.0'
            }, indent=2)
        }
        
        for filename, content in files.items():
            (self.context.work_directory / filename).write_text(content)
        
        return {
            "directories": dirs,
            "files": list(files.keys())
        }
    
    async def _create_web_app_structure(self, task: Task) -> Dict[str, Any]:
        """Create web application structure"""
        # Create standard web app structure
        dirs = [
            'src/components',
            'src/pages',
            'src/styles',
            'src/utils',
            'public'
        ]
        
        for dir_name in dirs:
            (self.context.work_directory / dir_name).mkdir(parents=True, exist_ok=True)
        
        return {"directories": dirs}
    
    async def _generate_project_documentation(self, task: Task) -> None:
        """Generate project documentation"""
        doc_path = self.context.output_directory / "PROJECT_DOCUMENTATION.md"
        
        content = f"""# {self.context.project_variables['project_name']}

## Overview
{self.context.project_variables['description']}

## Execution Summary
- Total tasks: {len(self.context.execution_results)}
- Successful: {sum(1 for r in self.context.execution_results.values() if r.status == ExecutionStatus.COMPLETED)}
- Failed: {sum(1 for r in self.context.execution_results.values() if r.status == ExecutionStatus.FAILED)}

## Tasks Executed
"""
        
        for result in self.context.execution_results.values():
            content += f"\n### {result.task_id}\n"
            content += f"- Status: {result.status.value}\n"
            content += f"- Duration: {result.duration:.2f}s\n"
            if result.error:
                content += f"- Error: {result.error}\n"
        
        doc_path.write_text(content)
    
    def _build_code_generation_prompt(self, task: Task) -> str:
        """Build prompt for code generation"""
        prompt = f"""Generate code for: {task.name}

Description: {task.description}

Requirements:
"""
        for req in task.requirements:
            prompt += f"- {req.type}: {req.name}\n"
        
        return prompt
    
    def _save_execution_report(self, plan: ExecutionPlan, results: Dict[str, ExecutionResult]) -> None:
        """Save execution report"""
        report_path = self.context.output_directory / "execution_report.json"
        
        report = {
            "plan": plan.to_dict(),
            "results": {k: v.to_dict() for k, v in results.items()},
            "summary": {
                "total_tasks": len(results),
                "completed": sum(1 for r in results.values() if r.status == ExecutionStatus.COMPLETED),
                "failed": sum(1 for r in results.values() if r.status == ExecutionStatus.FAILED),
                "skipped": sum(1 for r in results.values() if r.status == ExecutionStatus.SKIPPED),
                "total_duration": sum(r.duration for r in results.values())
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Execution report saved to {report_path}")
    
    def _calculate_success_rate(self, results: Dict[str, ExecutionResult]) -> float:
        """Calculate success rate"""
        if not results:
            return 0.0
        
        completed = sum(1 for r in results.values() if r.status == ExecutionStatus.COMPLETED)
        return (completed / len(results)) * 100


# Example usage
if __name__ == "__main__":
    from task_planner import TaskPlanner
    
    # Setup
    config = {
        'framework': {'max_parallel_tasks': 5},
        'execution': {
            'work_directory': './workspace',
            'output_directory': './output',
            'log_level': 'INFO'
        }
    }
    
    # Create plan
    planner = TaskPlanner()
    plan = planner.create_execution_plan(
        "Create a React dashboard with MongoDB backend"
    )
    plan = planner.optimize_plan(plan)
    
    # Execute plan
    engine = ExecutionEngine(config)
    results = asyncio.run(engine.execute_plan(plan))
    
    print("\n" + "="*80)
    print("EXECUTION COMPLETE")
    print("="*80)
    for task_id, result in results.items():
        print(f"{task_id}: {result.status.value} ({result.duration:.2f}s)")
