"""
Monitoring Dashboard for ByteClaude
Tracks execution metrics and provides real-time monitoring
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class ExecutionStatus(Enum):
    """Execution status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskMetrics:
    """Metrics for a single task"""
    task_id: str
    name: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    outputs: Dict[str, Any] = field(default_factory=dict)

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.elapsed_time,
            "errors": self.errors,
            "warnings": self.warnings
        }


@dataclass
class ExecutionMetrics:
    """Metrics for a complete execution"""
    execution_id: str
    workflow_name: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: ExecutionStatus = ExecutionStatus.RUNNING
    tasks: List[TaskMetrics] = field(default_factory=list)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_errors: int = 0
    total_warnings: int = 0

    @property
    def progress_percentage(self) -> float:
        """Get progress percentage"""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100

    @property
    def success_rate(self) -> float:
        """Get success rate"""
        if self.total_tasks == 0:
            return 100.0
        return ((self.total_tasks - self.failed_tasks) / self.total_tasks) * 100

    @property
    def total_duration(self) -> float:
        """Get total execution duration"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "execution_id": self.execution_id,
            "workflow_name": self.workflow_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.total_duration,
            "progress": self.progress_percentage,
            "success_rate": self.success_rate,
            "tasks": [t.to_dict() for t in self.tasks],
            "summary": {
                "total_tasks": self.total_tasks,
                "completed_tasks": self.completed_tasks,
                "failed_tasks": self.failed_tasks,
                "total_errors": self.total_errors,
                "total_warnings": self.total_warnings
            }
        }


class MonitoringDashboard:
    """
    Real-time monitoring dashboard for ByteClaude executions
    """

    def __init__(self):
        self.executions: Dict[str, ExecutionMetrics] = {}
        self.current_execution: Optional[str] = None

    def create_execution(
        self,
        execution_id: str,
        workflow_name: str,
        total_tasks: int
    ) -> ExecutionMetrics:
        """Create a new execution tracking record"""
        metrics = ExecutionMetrics(
            execution_id=execution_id,
            workflow_name=workflow_name,
            total_tasks=total_tasks
        )
        self.executions[execution_id] = metrics
        self.current_execution = execution_id
        return metrics

    def start_task(self, execution_id: str, task_id: str, task_name: str) -> TaskMetrics:
        """Record task start"""
        if execution_id not in self.executions:
            raise ValueError(f"Execution {execution_id} not found")

        task_metrics = TaskMetrics(
            task_id=task_id,
            name=task_name,
            status=ExecutionStatus.RUNNING,
            start_time=datetime.now()
        )

        self.executions[execution_id].tasks.append(task_metrics)
        return task_metrics

    def complete_task(
        self,
        execution_id: str,
        task_id: str,
        success: bool = True,
        errors: List[str] = None,
        warnings: List[str] = None
    ):
        """Record task completion"""
        if execution_id not in self.executions:
            raise ValueError(f"Execution {execution_id} not found")

        execution = self.executions[execution_id]
        task = next((t for t in execution.tasks if t.task_id == task_id), None)

        if not task:
            raise ValueError(f"Task {task_id} not found")

        task.end_time = datetime.now()
        task.status = ExecutionStatus.COMPLETED if success else ExecutionStatus.FAILED

        if errors:
            task.errors = errors
            execution.total_errors += len(errors)

        if warnings:
            task.warnings = warnings
            execution.total_warnings += len(warnings)

        execution.completed_tasks += 1
        if not success:
            execution.failed_tasks += 1

    def complete_execution(self, execution_id: str):
        """Mark execution as complete"""
        if execution_id not in self.executions:
            raise ValueError(f"Execution {execution_id} not found")

        execution = self.executions[execution_id]
        execution.end_time = datetime.now()
        execution.status = (
            ExecutionStatus.COMPLETED if execution.failed_tasks == 0
            else ExecutionStatus.FAILED
        )

    def get_execution_metrics(self, execution_id: str) -> Optional[ExecutionMetrics]:
        """Get execution metrics"""
        return self.executions.get(execution_id)

    def get_all_executions(self) -> List[ExecutionMetrics]:
        """Get all executions"""
        return list(self.executions.values())

    def get_current_execution(self) -> Optional[ExecutionMetrics]:
        """Get current execution metrics"""
        if self.current_execution:
            return self.executions.get(self.current_execution)
        return None

    def get_summary(self) -> Dict[str, Any]:
        """Get dashboard summary"""
        all_executions = self.get_all_executions()

        return {
            "total_executions": len(all_executions),
            "successful_executions": sum(
                1 for e in all_executions if e.status == ExecutionStatus.COMPLETED
            ),
            "failed_executions": sum(
                1 for e in all_executions if e.status == ExecutionStatus.FAILED
            ),
            "total_tasks_executed": sum(e.total_tasks for e in all_executions),
            "total_tasks_completed": sum(e.completed_tasks for e in all_executions),
            "total_errors": sum(e.total_errors for e in all_executions),
            "total_warnings": sum(e.total_warnings for e in all_executions),
            "average_duration": sum(e.total_duration for e in all_executions) / len(all_executions) if all_executions else 0,
            "timestamp": datetime.now().isoformat()
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        all_executions = self.get_all_executions()

        if not all_executions:
            return {}

        durations = [e.total_duration for e in all_executions]
        success_rates = [e.success_rate for e in all_executions]

        return {
            "avg_execution_time": sum(durations) / len(durations),
            "min_execution_time": min(durations),
            "max_execution_time": max(durations),
            "avg_success_rate": sum(success_rates) / len(success_rates),
            "total_tasks_per_execution": sum(e.total_tasks for e in all_executions) / len(all_executions)
        }

    def export_report(self, execution_id: str) -> Dict[str, Any]:
        """Export detailed execution report"""
        execution = self.get_execution_metrics(execution_id)

        if not execution:
            return {}

        return {
            "execution": execution.to_dict(),
            "summary": self.get_summary(),
            "performance": self.get_performance_stats()
        }


# Helper function
def create_dashboard() -> MonitoringDashboard:
    """Create a new monitoring dashboard"""
    return MonitoringDashboard()
