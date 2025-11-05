"""
Task Planner - Intelligent Task Decomposition and Planning
Converts natural language requests into structured execution plans
"""

import json
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    """Types of tasks the framework can handle"""
    FILE_OPERATION = "file_operation"
    CODE_GENERATION = "code_generation"
    DATA_PROCESSING = "data_processing"
    API_INTEGRATION = "api_integration"
    DOCUMENT_GENERATION = "document_generation"
    WEB_DEVELOPMENT = "web_development"
    DATABASE_OPERATION = "database_operation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    VALIDATION = "validation"


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class TaskRequirement:
    """Represents a capability or resource needed for a task"""
    type: str  # 'skill', 'mcp', 'context7'
    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    optional: bool = False


@dataclass
class Task:
    """Represents a single executable task"""
    id: str
    name: str
    description: str
    task_type: TaskType
    requirements: List[TaskRequirement] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    estimated_duration: int = 300  # seconds
    output_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'task_type': self.task_type.value,
            'requirements': [
                {'type': r.type, 'name': r.name, 'config': r.config, 'optional': r.optional}
                for r in self.requirements
            ],
            'dependencies': self.dependencies,
            'priority': self.priority.value,
            'estimated_duration': self.estimated_duration,
            'output_path': self.output_path,
            'metadata': self.metadata
        }


@dataclass
class ExecutionPlan:
    """Complete execution plan for a project"""
    project_name: str
    description: str
    tasks: List[Task]
    execution_order: List[str] = field(default_factory=list)
    estimated_total_duration: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary"""
        return {
            'project_name': self.project_name,
            'description': self.description,
            'tasks': [t.to_dict() for t in self.tasks],
            'execution_order': self.execution_order,
            'estimated_total_duration': self.estimated_total_duration,
            'metadata': self.metadata
        }
    
    def save(self, path: str):
        """Save execution plan to file"""
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)


class TaskPlanner:
    """
    Main task planning engine that:
    1. Analyzes natural language requests
    2. Decomposes into executable tasks
    3. Resolves dependencies
    4. Optimizes execution order
    """
    
    def __init__(self, config_path: str = "./config/framework-config.yaml"):
        self.config = self._load_config(config_path)
        self.available_skills = self._discover_skills()
        self.available_mcps = self._discover_mcps()
        
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load framework configuration"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default config
            return {
                'framework': {'max_parallel_tasks': 5},
                'execution': {
                    'work_directory': './workspace',
                    'output_directory': './output'
                }
            }
    
    def _discover_skills(self) -> List[str]:
        """Discover available skills"""
        # In real implementation, scan /mnt/skills directories
        return [
            'docx', 'pdf', 'pptx', 'xlsx', 'skill-creator',
            'artifacts-builder', 'theme-factory', 'mcp-builder', 'canvas-design'
        ]
    
    def _discover_mcps(self) -> List[str]:
        """Discover available MCPs"""
        return [
            'hubspot', 'chrome', 'mac_control', 'beeper', 'filesystem',
            'airtable', 'notion', 'mongodb', 'stripe', 'context7', 'youtube'
        ]
    
    def analyze_request(self, request: str) -> Dict[str, Any]:
        """
        Analyze natural language request to extract:
        - Project type
        - Required technologies
        - Key features
        - Constraints
        """
        analysis = {
            'project_type': self._identify_project_type(request),
            'technologies': self._extract_technologies(request),
            'features': self._extract_features(request),
            'constraints': self._extract_constraints(request),
            'required_mcps': [],
            'required_skills': [],
            'context7_libraries': []
        }
        
        # Map technologies to MCPs and skills
        tech_mcp_mapping = {
            'stripe': 'stripe',
            'payment': 'stripe',
            'notion': 'notion',
            'airtable': 'airtable',
            'mongodb': 'mongodb',
            'database': 'mongodb',
            'hubspot': 'hubspot',
            'crm': 'hubspot'
        }
        
        tech_skill_mapping = {
            'document': 'docx',
            'word': 'docx',
            'pdf': 'pdf',
            'presentation': 'pptx',
            'powerpoint': 'pptx',
            'spreadsheet': 'xlsx',
            'excel': 'xlsx',
            'web': 'artifacts-builder',
            'react': 'artifacts-builder',
            'persona': 'customer-persona-identification',
            'buyer persona': 'customer-persona-identification',
            'customer segment': 'customer-persona-identification',
            'icp': 'customer-persona-identification',
            'ideal customer profile': 'customer-persona-identification',
            'jobs to be done': 'customer-persona-identification',
            'jtbd': 'customer-persona-identification',
            'message market fit': 'customer-persona-identification',
            'customer analysis': 'customer-persona-identification',
            'market segmentation': 'customer-persona-identification',
            'target audience': 'customer-persona-identification',
            'customer profile': 'customer-persona-identification'
        }
        
        request_lower = request.lower()
        
        # Identify required MCPs
        for tech, mcp in tech_mcp_mapping.items():
            if tech in request_lower:
                analysis['required_mcps'].append(mcp)
        
        # Identify required skills
        for tech, skill in tech_skill_mapping.items():
            if tech in request_lower:
                analysis['required_skills'].append(skill)
        
        # Identify Context7 libraries needed
        context7_mapping = {
            'react': 'react',
            'next.js': 'next.js',
            'nextjs': 'next.js',
            'vue': 'vue',
            'mongodb': 'mongodb',
            'stripe': 'stripe',
            'tailwind': 'tailwindcss'
        }
        
        for tech, lib in context7_mapping.items():
            if tech in request_lower:
                analysis['context7_libraries'].append(lib)
        
        return analysis
    
    def _identify_project_type(self, request: str) -> str:
        """Identify the type of project from request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['app', 'application', 'web', 'dashboard']):
            return 'web_application'
        elif any(word in request_lower for word in ['document', 'report', 'pdf', 'docx']):
            return 'document_generation'
        elif any(word in request_lower for word in ['api', 'integration', 'sync']):
            return 'api_integration'
        elif any(word in request_lower for word in ['pipeline', 'automation', 'workflow']):
            return 'data_pipeline'
        else:
            return 'general'
    
    def _extract_technologies(self, request: str) -> List[str]:
        """Extract technology stack from request"""
        technologies = []
        tech_keywords = {
            'react', 'vue', 'angular', 'next.js', 'nextjs', 'svelte',
            'node', 'python', 'typescript', 'javascript',
            'mongodb', 'postgres', 'mysql',
            'stripe', 'notion', 'airtable'
        }
        
        request_lower = request.lower()
        for tech in tech_keywords:
            if tech in request_lower:
                technologies.append(tech)
        
        return technologies
    
    def _extract_features(self, request: str) -> List[str]:
        """Extract key features from request"""
        features = []
        feature_keywords = {
            'authentication': ['auth', 'login', 'signup'],
            'payment': ['payment', 'checkout', 'stripe'],
            'database': ['database', 'data', 'store'],
            'api': ['api', 'endpoint', 'rest'],
            'ui': ['ui', 'interface', 'dashboard', 'design'],
            'search': ['search', 'filter', 'query'],
            'notification': ['notification', 'alert', 'email']
        }
        
        request_lower = request.lower()
        for feature, keywords in feature_keywords.items():
            if any(kw in request_lower for kw in keywords):
                features.append(feature)
        
        return features
    
    def _extract_constraints(self, request: str) -> Dict[str, Any]:
        """Extract constraints like deadlines, budget, etc."""
        constraints = {}
        
        # Look for time constraints
        if 'urgent' in request.lower() or 'asap' in request.lower():
            constraints['priority'] = 'high'
        
        # Look for testing requirements
        if 'test' in request.lower():
            constraints['include_tests'] = True
        
        return constraints
    
    def create_execution_plan(self, request: str) -> ExecutionPlan:
        """
        Create a complete execution plan from natural language request
        """
        # Analyze the request
        analysis = self.analyze_request(request)
        
        # Generate project name
        project_name = self._generate_project_name(request)
        
        # Create tasks based on analysis
        tasks = self._generate_tasks(analysis, request)
        
        # Resolve dependencies
        execution_order = self._resolve_dependencies(tasks)
        
        # Calculate duration
        total_duration = sum(task.estimated_duration for task in tasks)
        
        plan = ExecutionPlan(
            project_name=project_name,
            description=request,
            tasks=tasks,
            execution_order=execution_order,
            estimated_total_duration=total_duration,
            metadata=analysis
        )
        
        return plan
    
    def _generate_project_name(self, request: str) -> str:
        """Generate a project name from request"""
        # Simple implementation - in production, use better naming
        words = request.split()[:3]
        name = '-'.join(w.lower() for w in words if w.isalnum())
        return name or 'project'
    
    def _generate_tasks(self, analysis: Dict[str, Any], request: str) -> List[Task]:
        """Generate tasks based on analysis"""
        tasks = []
        task_counter = 0
        
        # Task 1: Setup and scaffolding
        task_counter += 1
        tasks.append(Task(
            id=f"task_{task_counter}",
            name="Project Setup",
            description="Initialize project structure and configuration",
            task_type=TaskType.FILE_OPERATION,
            requirements=[
                TaskRequirement(type='skill', name='skill-creator', config={})
            ],
            priority=Priority.CRITICAL,
            estimated_duration=120
        ))
        
        # Task 2: Fetch documentation if needed
        if analysis['context7_libraries']:
            task_counter += 1
            tasks.append(Task(
                id=f"task_{task_counter}",
                name="Fetch Documentation",
                description="Retrieve relevant documentation from Context7",
                task_type=TaskType.API_INTEGRATION,
                requirements=[
                    TaskRequirement(
                        type='context7',
                        name='context7',
                        config={'libraries': analysis['context7_libraries']}
                    )
                ],
                dependencies=[tasks[0].id],
                priority=Priority.HIGH,
                estimated_duration=60
            ))
        
        # Task 3: Core development
        if analysis['project_type'] == 'web_application':
            task_counter += 1
            requirements = []
            
            if 'artifacts-builder' in analysis['required_skills']:
                requirements.append(
                    TaskRequirement(type='skill', name='artifacts-builder')
                )
            
            for mcp in analysis['required_mcps']:
                requirements.append(
                    TaskRequirement(type='mcp', name=mcp)
                )
            
            tasks.append(Task(
                id=f"task_{task_counter}",
                name="Develop Application",
                description="Build the main application components",
                task_type=TaskType.WEB_DEVELOPMENT,
                requirements=requirements,
                dependencies=[tasks[0].id],
                priority=Priority.CRITICAL,
                estimated_duration=1800
            ))
        
        elif analysis['project_type'] == 'document_generation':
            task_counter += 1
            skill_name = next(
                (s for s in analysis['required_skills'] if s in ['docx', 'pdf', 'pptx', 'xlsx']),
                'docx'
            )
            
            tasks.append(Task(
                id=f"task_{task_counter}",
                name="Generate Documents",
                description="Create document outputs",
                task_type=TaskType.DOCUMENT_GENERATION,
                requirements=[
                    TaskRequirement(type='skill', name=skill_name)
                ],
                dependencies=[tasks[0].id],
                priority=Priority.CRITICAL,
                estimated_duration=600
            ))
        
        # Task 4: Integration tasks
        if len(analysis['required_mcps']) > 1:
            task_counter += 1
            tasks.append(Task(
                id=f"task_{task_counter}",
                name="Integrate External Services",
                description="Connect and configure external API integrations",
                task_type=TaskType.API_INTEGRATION,
                requirements=[
                    TaskRequirement(type='mcp', name=mcp)
                    for mcp in analysis['required_mcps']
                ],
                dependencies=[t.id for t in tasks if t.task_type == TaskType.WEB_DEVELOPMENT],
                priority=Priority.HIGH,
                estimated_duration=900
            ))
        
        # Task 5: Testing
        if analysis['constraints'].get('include_tests', False):
            task_counter += 1
            tasks.append(Task(
                id=f"task_{task_counter}",
                name="Generate Tests",
                description="Create automated tests",
                task_type=TaskType.TESTING,
                requirements=[],
                dependencies=[t.id for t in tasks if t.task_type in [
                    TaskType.WEB_DEVELOPMENT,
                    TaskType.CODE_GENERATION
                ]],
                priority=Priority.MEDIUM,
                estimated_duration=600
            ))
        
        # Task 6: Validation and documentation
        task_counter += 1
        tasks.append(Task(
            id=f"task_{task_counter}",
            name="Validation and Documentation",
            description="Validate outputs and generate documentation",
            task_type=TaskType.VALIDATION,
            requirements=[
                TaskRequirement(type='skill', name='docx', config={'doc_type': 'README'})
            ],
            dependencies=[t.id for t in tasks[1:]],  # Depends on all previous tasks
            priority=Priority.MEDIUM,
            estimated_duration=300
        ))
        
        return tasks
    
    def _resolve_dependencies(self, tasks: List[Task]) -> List[str]:
        """
        Resolve task dependencies and determine execution order
        Uses topological sort for dependency resolution
        """
        # Build dependency graph
        task_map = {task.id: task for task in tasks}
        in_degree = {task.id: 0 for task in tasks}
        
        # Calculate in-degrees
        for task in tasks:
            for dep in task.dependencies:
                if dep in in_degree:
                    in_degree[task.id] += 1
        
        # Find tasks with no dependencies
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        execution_order = []
        
        while queue:
            # Sort by priority
            queue.sort(key=lambda tid: task_map[tid].priority.value)
            current = queue.pop(0)
            execution_order.append(current)
            
            # Update in-degrees for dependent tasks
            for task in tasks:
                if current in task.dependencies:
                    in_degree[task.id] -= 1
                    if in_degree[task.id] == 0:
                        queue.append(task.id)
        
        return execution_order
    
    def optimize_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        """
        Optimize execution plan for:
        - Parallel execution opportunities
        - Resource utilization
        - Critical path optimization
        """
        # Find tasks that can run in parallel
        parallel_groups = []
        current_group = []
        
        for task_id in plan.execution_order:
            task = next(t for t in plan.tasks if t.id == task_id)
            
            # Check if task can be added to current parallel group
            can_parallelize = True
            for group_task_id in current_group:
                group_task = next(t for t in plan.tasks if t.id == group_task_id)
                # Check for dependency conflicts
                if task_id in group_task.dependencies or group_task_id in task.dependencies:
                    can_parallelize = False
                    break
            
            if can_parallelize and len(current_group) < self.config['framework']['max_parallel_tasks']:
                current_group.append(task_id)
            else:
                if current_group:
                    parallel_groups.append(current_group)
                current_group = [task_id]
        
        if current_group:
            parallel_groups.append(current_group)
        
        plan.metadata['parallel_groups'] = parallel_groups
        
        # Recalculate duration based on parallel execution
        optimized_duration = 0
        for group in parallel_groups:
            group_duration = max(
                next(t for t in plan.tasks if t.id == tid).estimated_duration
                for tid in group
            )
            optimized_duration += group_duration
        
        plan.estimated_total_duration = optimized_duration
        
        return plan


# Example usage
if __name__ == "__main__":
    planner = TaskPlanner()
    
    # Example requests
    requests = [
        "Create a Next.js dashboard with Stripe payment integration and MongoDB backend",
        "Generate a monthly PDF report from Airtable data",
        "Build a React app with Notion integration for task management"
    ]
    
    for req in requests:
        print(f"\n{'='*80}")
        print(f"Request: {req}")
        print('='*80)
        
        plan = planner.create_execution_plan(req)
        plan = planner.optimize_plan(plan)
        
        print(f"\nProject: {plan.project_name}")
        print(f"Total Tasks: {len(plan.tasks)}")
        print(f"Estimated Duration: {plan.estimated_total_duration // 60} minutes")
        print(f"\nExecution Plan:")
        
        for i, task_id in enumerate(plan.execution_order, 1):
            task = next(t for t in plan.tasks if t.id == task_id)
            print(f"  {i}. {task.name} ({task.task_type.value})")
            if task.dependencies:
                print(f"     Dependencies: {', '.join(task.dependencies)}")
            print(f"     Requirements: {', '.join(r.name for r in task.requirements)}")
        
        if 'parallel_groups' in plan.metadata:
            print(f"\nParallel Execution Groups:")
            for i, group in enumerate(plan.metadata['parallel_groups'], 1):
                tasks_in_group = [next(t for t in plan.tasks if t.id == tid).name for tid in group]
                print(f"  Group {i}: {', '.join(tasks_in_group)}")
