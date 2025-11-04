"""
Workflow Designer - Visual Workflow Creation and Management
Converts between YAML execution plans and visual representations
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import yaml
from enum import Enum


class NodeType(Enum):
    """Types of workflow nodes"""
    TASK = "task"
    DECISION = "decision"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    START = "start"
    END = "end"


@dataclass
class WorkflowNode:
    """Represents a node in the workflow"""
    id: str
    type: NodeType
    title: str
    description: str = ""
    config: Dict[str, Any] = None
    inputs: List[str] = None
    outputs: List[str] = None
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'type': self.type.value,
            'title': self.title,
            'description': self.description,
            'config': self.config or {},
            'inputs': self.inputs or [],
            'outputs': self.outputs or [],
            'dependencies': self.dependencies or [],
            'metadata': self.metadata or {}
        }


@dataclass
class WorkflowConnection:
    """Represents a connection between nodes"""
    source_id: str
    target_id: str
    label: str = ""
    condition: str = ""
    metadata: Dict[str, Any] = None


class WorkflowDesigner:
    """
    Visual workflow designer for creating and managing execution workflows
    """

    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.connections: List[WorkflowConnection] = []
        self.metadata: Dict[str, Any] = {}

    def add_node(
        self,
        node_id: str,
        node_type: NodeType,
        title: str,
        description: str = "",
        config: Dict[str, Any] = None
    ) -> WorkflowNode:
        """Add a node to the workflow"""
        node = WorkflowNode(
            id=node_id,
            type=node_type,
            title=title,
            description=description,
            config=config or {}
        )
        self.nodes[node_id] = node
        return node

    def connect_nodes(
        self,
        source_id: str,
        target_id: str,
        label: str = "",
        condition: str = ""
    ) -> WorkflowConnection:
        """Connect two nodes"""
        connection = WorkflowConnection(
            source_id=source_id,
            target_id=target_id,
            label=label,
            condition=condition
        )
        self.connections.append(connection)
        return connection

    def get_execution_order(self) -> List[str]:
        """Get topologically sorted execution order"""
        # Simple topological sort
        visited = set()
        order = []

        def visit(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)

            # Visit dependencies
            for conn in self.connections:
                if conn.target_id == node_id:
                    visit(conn.source_id)

            order.append(node_id)

        for node_id in self.nodes:
            visit(node_id)

        return order

    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary"""
        return {
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'connections': [
                {
                    'source': c.source_id,
                    'target': c.target_id,
                    'label': c.label,
                    'condition': c.condition
                }
                for c in self.connections
            ],
            'metadata': self.metadata
        }

    def to_yaml(self) -> str:
        """Convert to YAML format"""
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def to_json(self) -> str:
        """Convert to JSON format"""
        return json.dumps(self.to_dict(), indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WorkflowDesigner':
        """Create workflow from dictionary"""
        designer = WorkflowDesigner()
        designer.metadata = data.get('metadata', {})

        # Add nodes
        for node_id, node_data in data.get('nodes', {}).items():
            designer.add_node(
                node_id,
                NodeType(node_data['type']),
                node_data['title'],
                node_data.get('description', ''),
                node_data.get('config', {})
            )

        # Add connections
        for conn_data in data.get('connections', []):
            designer.connect_nodes(
                conn_data['source'],
                conn_data['target'],
                conn_data.get('label', ''),
                conn_data.get('condition', '')
            )

        return designer

    def generate_diagram(self) -> str:
        """Generate ASCII diagram of workflow"""
        lines = []
        lines.append("┌─ WORKFLOW DIAGRAM ─────────────────────────┐")
        lines.append("│                                             │")

        for node_id in self.get_execution_order():
            node = self.nodes[node_id]
            lines.append(f"│  [{node.type.value.upper()}] {node.title}")
            if node.description:
                lines.append(f"│    └─ {node.description}")

        lines.append("│                                             │")
        lines.append("└─────────────────────────────────────────────┘")

        return "\n".join(lines)

    def validate(self) -> tuple[bool, List[str]]:
        """Validate workflow structure"""
        errors = []

        # Check for orphaned nodes
        connected_nodes = set()
        for conn in self.connections:
            connected_nodes.add(conn.source_id)
            connected_nodes.add(conn.target_id)

        for node_id in self.nodes:
            if node_id not in connected_nodes and self.nodes[node_id].type != NodeType.START:
                errors.append(f"Node '{node_id}' is not connected")

        # Check for cycles (simple check)
        # This is a simplified cycle detection
        for start_node in self.nodes:
            visited = set()
            if self._has_cycle(start_node, visited):
                errors.append(f"Cycle detected involving node '{start_node}'")
                break

        return len(errors) == 0, errors

    def _has_cycle(self, node_id: str, visited: set) -> bool:
        """Check if there's a cycle from this node"""
        if node_id in visited:
            return True

        visited.add(node_id)

        for conn in self.connections:
            if conn.source_id == node_id:
                if self._has_cycle(conn.target_id, visited.copy()):
                    return True

        return False


class WorkflowBuilder:
    """
    Helper class for building workflows with fluent interface
    """

    def __init__(self):
        self.designer = WorkflowDesigner()

    def start(self, title: str = "Start") -> 'WorkflowBuilder':
        """Add start node"""
        self.designer.add_node("start", NodeType.START, title)
        return self

    def task(
        self,
        task_id: str,
        title: str,
        description: str = "",
        config: Dict[str, Any] = None
    ) -> 'WorkflowBuilder':
        """Add task node"""
        self.designer.add_node(task_id, NodeType.TASK, title, description, config)
        return self

    def connect(
        self,
        source_id: str,
        target_id: str,
        label: str = ""
    ) -> 'WorkflowBuilder':
        """Connect two nodes"""
        self.designer.connect_nodes(source_id, target_id, label)
        return self

    def end(self, title: str = "End") -> 'WorkflowBuilder':
        """Add end node"""
        self.designer.add_node("end", NodeType.END, title)
        return self

    def build(self) -> WorkflowDesigner:
        """Build and return the workflow"""
        return self.designer


# Example usage helper
def create_example_workflow() -> WorkflowDesigner:
    """Create an example workflow"""
    builder = WorkflowBuilder()
    
    workflow = (
        builder
        .start()
        .task("analyze", "Analyze Requirements", "Understand project scope")
        .task("plan", "Create Execution Plan", "Decompose into tasks")
        .task("execute", "Execute Tasks", "Run implementation")
        .task("validate", "Validate Output", "Quality assurance")
        .end()
        .connect("start", "analyze")
        .connect("analyze", "plan")
        .connect("plan", "execute")
        .connect("execute", "validate")
        .connect("validate", "end")
        .build()
    )

    return workflow
