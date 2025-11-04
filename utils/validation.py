"""
Validation Utilities
Code quality, security, and best practices validation for ByteClaude framework
"""

import re
import ast
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Validation issue severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: Severity
    category: str
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    file: Optional[str] = None
    suggestion: Optional[str] = None
    code: Optional[str] = None


class CodeValidator:
    """
    Validates code quality and best practices
    """

    # Common code smells to detect
    CODE_SMELLS = {
        'long_function': 50,  # Max lines in a function
        'too_many_args': 5,   # Max function arguments
        'complex_condition': 3,  # Max nested if statements
        'magic_numbers': True,  # Detect magic numbers
    }

    # Security patterns to detect
    SECURITY_PATTERNS = [
        (r'eval\s*\(', "Use of eval() is dangerous"),
        (r'exec\s*\(', "Use of exec() is dangerous"),
        (r'__import__\s*\(', "Direct use of __import__() can be unsafe"),
        (r'pickle\.loads?\s*\(', "Pickle can execute arbitrary code"),
        (r'input\s*\([^)]*\)', "Direct input() usage can be dangerous"),
    ]

    # Best practice patterns
    BEST_PRACTICES = {
        'python': [
            (r'except\s*:', "Bare except clause - catch specific exceptions"),
            (r'print\s*\(', "Use logging instead of print"),
            (r'from\s+\w+\s+import\s+\*', "Avoid wildcard imports"),
        ],
        'javascript': [
            (r'var\s+', "Use 'let' or 'const' instead of 'var'"),
            (r'==(?!=)', "Use '===' for comparison"),
            (r'!=(?!=)', "Use '!==' for comparison"),
        ],
        'typescript': [
            (r':\s*any\s*[,;)]', "Avoid using 'any' type"),
        ]
    }

    def __init__(self, strict: bool = False):
        """
        Initialize CodeValidator

        Args:
            strict: Whether to treat warnings as errors
        """
        self.strict = strict
        self.issues: List[ValidationIssue] = []

    def validate_python_code(self, code: str, filename: str = "<string>") -> List[ValidationIssue]:
        """
        Validate Python code

        Args:
            code: Python code to validate
            filename: Filename for error reporting

        Returns:
            List of validation issues
        """
        self.issues = []

        # Check syntax
        try:
            tree = ast.parse(code, filename=filename)
            self._check_ast(tree, filename)
        except SyntaxError as e:
            self.issues.append(ValidationIssue(
                severity=Severity.CRITICAL,
                category="syntax",
                message=f"Syntax error: {e.msg}",
                line=e.lineno,
                column=e.offset,
                file=filename
            ))
            return self.issues

        # Check security issues
        self._check_security(code, filename, 'python')

        # Check best practices
        self._check_best_practices(code, filename, 'python')

        # Check style issues
        self._check_style(code, filename, 'python')

        return self.issues

    def validate_javascript_code(self, code: str, filename: str = "<string>") -> List[ValidationIssue]:
        """
        Validate JavaScript code

        Args:
            code: JavaScript code to validate
            filename: Filename for error reporting

        Returns:
            List of validation issues
        """
        self.issues = []

        # Check best practices
        self._check_best_practices(code, filename, 'javascript')

        # Check security
        self._check_security(code, filename, 'javascript')

        # Check for console.log
        if re.search(r'console\.log\s*\(', code):
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                category="debugging",
                message="Remove console.log() before production",
                file=filename,
                suggestion="Use a proper logging library"
            ))

        return self.issues

    def _check_ast(self, tree: ast.AST, filename: str) -> None:
        """Check AST for code quality issues"""
        for node in ast.walk(tree):
            # Check function complexity
            if isinstance(node, ast.FunctionDef):
                self._check_function(node, filename)

            # Check for magic numbers
            if isinstance(node, ast.Num) and not isinstance(node.n, (bool, type(None))):
                if self.CODE_SMELLS['magic_numbers']:
                    # Ignore common constants
                    if node.n not in [0, 1, -1, 2]:
                        self.issues.append(ValidationIssue(
                            severity=Severity.INFO,
                            category="maintainability",
                            message=f"Magic number detected: {node.n}",
                            line=node.lineno,
                            file=filename,
                            suggestion="Consider defining as a named constant"
                        ))

    def _check_function(self, node: ast.FunctionDef, filename: str) -> None:
        """Check function for quality issues"""
        # Count lines
        if hasattr(node, 'end_lineno') and node.end_lineno:
            lines = node.end_lineno - node.lineno
            if lines > self.CODE_SMELLS['long_function']:
                self.issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="complexity",
                    message=f"Function '{node.name}' is too long ({lines} lines)",
                    line=node.lineno,
                    file=filename,
                    suggestion="Consider breaking into smaller functions"
                ))

        # Count arguments
        arg_count = len(node.args.args)
        if arg_count > self.CODE_SMELLS['too_many_args']:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                category="complexity",
                message=f"Function '{node.name}' has too many arguments ({arg_count})",
                line=node.lineno,
                file=filename,
                suggestion="Consider using a configuration object or dataclass"
            ))

        # Check for deeply nested conditions
        max_depth = self._get_max_nesting_depth(node)
        if max_depth > self.CODE_SMELLS['complex_condition']:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                category="complexity",
                message=f"Function '{node.name}' has deeply nested conditions (depth: {max_depth})",
                line=node.lineno,
                file=filename,
                suggestion="Refactor to reduce nesting"
            ))

    def _get_max_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth of conditions"""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                child_depth = self._get_max_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._get_max_nesting_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _check_security(self, code: str, filename: str, language: str) -> None:
        """Check for security issues"""
        lines = code.split('\n')

        for pattern, message in self.SECURITY_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        category="security",
                        message=message,
                        line=i,
                        file=filename,
                        code=line.strip()
                    ))

    def _check_best_practices(self, code: str, filename: str, language: str) -> None:
        """Check for best practice violations"""
        if language not in self.BEST_PRACTICES:
            return

        lines = code.split('\n')

        for pattern, message in self.BEST_PRACTICES[language]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    self.issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        category="best_practices",
                        message=message,
                        line=i,
                        file=filename,
                        code=line.strip()
                    ))

    def _check_style(self, code: str, filename: str, language: str) -> None:
        """Check code style"""
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 120:
                self.issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    category="style",
                    message=f"Line too long ({len(line)} > 120 characters)",
                    line=i,
                    file=filename
                ))

            # Check trailing whitespace
            if line.rstrip() != line:
                self.issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    category="style",
                    message="Trailing whitespace",
                    line=i,
                    file=filename
                ))

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        summary = {
            'total_issues': len(self.issues),
            'by_severity': {},
            'by_category': {},
            'critical_count': 0,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0
        }

        for issue in self.issues:
            # Count by severity
            severity = issue.severity.value
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1

            # Count by category
            category = issue.category
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1

            # Quick counts
            if issue.severity == Severity.CRITICAL:
                summary['critical_count'] += 1
            elif issue.severity == Severity.ERROR:
                summary['error_count'] += 1
            elif issue.severity == Severity.WARNING:
                summary['warning_count'] += 1
            elif issue.severity == Severity.INFO:
                summary['info_count'] += 1

        return summary


class SecurityValidator:
    """
    Validates security aspects of code and configurations
    """

    # Known vulnerable patterns
    VULNERABLE_PATTERNS = {
        'hardcoded_password': r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
        'hardcoded_api_key': r'(api_key|apikey|api_secret)\s*=\s*["\'][^"\']+["\']',
        'hardcoded_token': r'(token|auth_token|access_token)\s*=\s*["\'][^"\']+["\']',
        'sql_injection': r'(execute|cursor\.execute|query)\s*\(["\'].*%s.*["\']',
        'command_injection': r'(os\.system|subprocess\.call|shell=True)',
    }

    # Sensitive file patterns
    SENSITIVE_FILES = [
        '.env',
        'credentials.json',
        'secrets.yaml',
        'private_key',
        'id_rsa',
        '*.pem',
        '*.key'
    ]

    def __init__(self):
        """Initialize SecurityValidator"""
        self.issues: List[ValidationIssue] = []

    def scan_code(self, code: str, filename: str = "<string>") -> List[ValidationIssue]:
        """
        Scan code for security vulnerabilities

        Args:
            code: Code to scan
            filename: Filename for reporting

        Returns:
            List of security issues
        """
        self.issues = []
        lines = code.split('\n')

        for pattern_name, pattern in self.VULNERABLE_PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(ValidationIssue(
                        severity=Severity.CRITICAL,
                        category="security",
                        message=f"Potential {pattern_name.replace('_', ' ')} detected",
                        line=i,
                        file=filename,
                        code=line.strip(),
                        suggestion=f"Remove {pattern_name.replace('_', ' ')} and use environment variables"
                    ))

        return self.issues

    def check_dependencies(self, requirements: List[str]) -> List[ValidationIssue]:
        """
        Check for known vulnerable dependencies

        Args:
            requirements: List of package requirements

        Returns:
            List of security issues
        """
        # This would integrate with a vulnerability database
        # For now, just a simple implementation
        self.issues = []

        # Example: check for unpinned versions
        for req in requirements:
            if '==' not in req and '>=' not in req:
                self.issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="dependency",
                    message=f"Unpinned dependency: {req}",
                    suggestion="Pin dependency versions for reproducible builds"
                ))

        return self.issues

    def check_file_permissions(self, file_path: Path) -> List[ValidationIssue]:
        """
        Check file permissions for security issues

        Args:
            file_path: Path to file

        Returns:
            List of security issues
        """
        self.issues = []

        # Check if file is world-readable/writable
        try:
            mode = file_path.stat().st_mode
            if mode & 0o004:  # World readable
                self.issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="permissions",
                    message=f"File is world-readable: {file_path}",
                    suggestion="Restrict file permissions"
                ))

            if mode & 0o002:  # World writable
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="permissions",
                    message=f"File is world-writable: {file_path}",
                    suggestion="Remove world-write permission"
                ))
        except OSError:
            pass

        return self.issues


# Convenience functions
def validate_python_file(file_path: str, strict: bool = False) -> Tuple[List[ValidationIssue], Dict[str, Any]]:
    """
    Validate a Python file

    Args:
        file_path: Path to Python file
        strict: Whether to use strict validation

    Returns:
        Tuple of (issues list, summary dict)
    """
    path = Path(file_path)
    code = path.read_text()

    validator = CodeValidator(strict=strict)
    issues = validator.validate_python_code(code, str(path))
    summary = validator.get_summary()

    return issues, summary


def scan_for_secrets(code: str) -> List[ValidationIssue]:
    """
    Quick scan for potential secrets in code

    Args:
        code: Code to scan

    Returns:
        List of potential secret issues
    """
    validator = SecurityValidator()
    return validator.scan_code(code)
