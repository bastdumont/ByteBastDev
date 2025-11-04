"""
Template Engine Utility
Jinja2-style template rendering for code and file generation
"""

import re
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path


class TemplateEngine:
    """
    Simple but powerful template engine for code generation
    """

    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize TemplateEngine

        Args:
            template_dir: Directory containing templates
        """
        self.template_dir = Path(template_dir) if template_dir else None
        self.filters: Dict[str, Callable] = self._register_default_filters()
        self.globals: Dict[str, Any] = {}

    def render(
        self,
        template: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render template with variables

        Args:
            template: Template string
            variables: Variables to use in template

        Returns:
            Rendered template
        """
        vars_dict = {**self.globals, **(variables or {})}

        # Process conditionals
        rendered = self._process_conditionals(template, vars_dict)

        # Process loops
        rendered = self._process_loops(rendered, vars_dict)

        # Process variables
        rendered = self._process_variables(rendered, vars_dict)

        # Process filters
        rendered = self._process_filters(rendered, vars_dict)

        return rendered

    def render_file(
        self,
        template_name: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render template from file

        Args:
            template_name: Template filename
            variables: Variables to use

        Returns:
            Rendered template
        """
        if not self.template_dir:
            raise ValueError("Template directory not set")

        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        template = template_path.read_text()
        return self.render(template, variables)

    def add_filter(self, name: str, func: Callable):
        """
        Add a custom filter

        Args:
            name: Filter name
            func: Filter function
        """
        self.filters[name] = func

    def set_global(self, name: str, value: Any):
        """
        Set a global variable

        Args:
            name: Variable name
            value: Variable value
        """
        self.globals[name] = value

    def _process_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Process {{ variable }} syntax"""
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\}\}'

        def replace(match):
            var_name = match.group(1)
            value = self._get_variable(var_name, variables)
            return str(value) if value is not None else ''

        return re.sub(pattern, replace, template)

    def _process_conditionals(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Process {% if condition %} ... {% endif %} syntax
        """
        pattern = r'\{%\s*if\s+(.+?)\s*%\}(.*?)\{%\s*endif\s*%\}'

        def replace(match):
            condition = match.group(1).strip()
            content = match.group(2)

            # Evaluate condition
            if self._evaluate_condition(condition, variables):
                return content
            else:
                return ''

        # Handle nested conditionals by processing from innermost
        while re.search(pattern, template, re.DOTALL):
            template = re.sub(pattern, replace, template, flags=re.DOTALL)

        return template

    def _process_loops(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Process {% for item in items %} ... {% endfor %} syntax
        """
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'

        def replace(match):
            item_var = match.group(1)
            list_var = match.group(2)
            content = match.group(3)

            items = variables.get(list_var, [])
            if not isinstance(items, list):
                return ''

            results = []
            for item in items:
                # Create context with loop variable
                loop_vars = {**variables, item_var: item}
                # Recursively render content with loop variable
                rendered = self.render(content, loop_vars)
                results.append(rendered)

            return ''.join(results)

        # Process loops (may be nested)
        while re.search(pattern, template, re.DOTALL):
            template = re.sub(pattern, replace, template, flags=re.DOTALL)

        return template

    def _process_filters(self, template: str, variables: Dict[str, Any]) -> str:
        """Process {{ variable|filter }} syntax"""
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\|\s*(\w+)\s*\}\}'

        def replace(match):
            var_name = match.group(1)
            filter_name = match.group(2)

            value = self._get_variable(var_name, variables)

            if filter_name in self.filters:
                value = self.filters[filter_name](value)

            return str(value) if value is not None else ''

        return re.sub(pattern, replace, template)

    def _evaluate_condition(self, condition: str, variables: Dict[str, Any]) -> bool:
        """Evaluate a simple condition"""
        # Handle negation
        negated = False
        if condition.startswith('not '):
            negated = True
            condition = condition[4:].strip()

        # Check if variable exists and is truthy
        value = self._get_variable(condition, variables)
        result = bool(value)

        return not result if negated else result

    def _get_variable(self, var_path: str, variables: Dict[str, Any]) -> Any:
        """Get variable value with support for dot notation"""
        parts = var_path.split('.')
        value = variables

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

        return value

    def _register_default_filters(self) -> Dict[str, Callable]:
        """Register default filters"""
        return {
            'upper': lambda x: str(x).upper() if x else '',
            'lower': lambda x: str(x).lower() if x else '',
            'capitalize': lambda x: str(x).capitalize() if x else '',
            'title': lambda x: str(x).title() if x else '',
            'strip': lambda x: str(x).strip() if x else '',
            'length': lambda x: len(x) if hasattr(x, '__len__') else 0,
            'first': lambda x: x[0] if x and hasattr(x, '__getitem__') else '',
            'last': lambda x: x[-1] if x and hasattr(x, '__getitem__') else '',
            'join': lambda x: ', '.join(str(i) for i in x) if hasattr(x, '__iter__') else str(x),
            'default': lambda x: x if x else 'N/A',
        }


# Convenience function
def render_template(template: str, **variables) -> str:
    """
    Quick template rendering

    Args:
        template: Template string
        **variables: Template variables

    Returns:
        Rendered template
    """
    engine = TemplateEngine()
    return engine.render(template, variables)
