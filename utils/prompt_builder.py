"""
Prompt Builder Utility
Dynamic prompt construction with templates, variables, and best practices
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from enum import Enum
import re


class PromptStyle(Enum):
    """Prompt style presets"""
    EXPERT = "expert"
    BEGINNER = "beginner"
    CONCISE = "concise"
    DETAILED = "detailed"
    CONVERSATIONAL = "conversational"


class PromptBuilder:
    """
    Build sophisticated prompts for Claude with templates and best practices
    """

    # Common prompt patterns
    PATTERNS = {
        'chain_of_thought': """Let's approach this step by step:
1. First, analyze the requirements
2. Then, design the solution
3. Finally, implement the code""",

        'expert_system': """You are an expert {domain} engineer with {years} years of experience.
Your expertise includes: {expertise}

Task: {task}

Requirements:
{requirements}

Best practices to follow:
{best_practices}""",

        'code_review': """Perform a comprehensive code review focusing on:
- Code quality and maintainability
- Performance and optimization
- Security vulnerabilities
- Best practices compliance
- Type safety
- Error handling
- Documentation quality

Code to review:
```{language}
{code}
```

Provide specific, actionable feedback with examples.""",

        'debug_assistant': """I'm experiencing an issue with my {language} code.

Problem: {problem}

Expected behavior: {expected}
Actual behavior: {actual}

Code:
```{language}
{code}
```

Error message (if any):
```
{error}
```

Please help me:
1. Identify the root cause
2. Explain why it's happening
3. Provide a fix with explanation
4. Suggest how to prevent similar issues""",

        'architecture_design': """Design a software architecture for:

System: {system_name}
Purpose: {purpose}
Scale: {scale}
Constraints: {constraints}

Requirements:
{requirements}

Please provide:
1. High-level architecture diagram (described in text)
2. Component breakdown with responsibilities
3. Data flow and interactions
4. Technology recommendations with justifications
5. Scalability considerations
6. Security considerations""",

        'optimization': """Optimize this {language} code for {goal}:

Current code:
```{language}
{code}
```

Performance requirements:
{requirements}

Please provide:
1. Analysis of current performance bottlenecks
2. Optimized version with explanations
3. Performance comparison (estimated)
4. Trade-offs made""",

        'test_generation': """Generate comprehensive tests for this {language} code:

```{language}
{code}
```

Test requirements:
- Unit tests with edge cases
- Integration tests if applicable
- Mocking examples for external dependencies
- Test coverage > {coverage}%
- Use {framework} framework

Include:
1. Test setup and fixtures
2. Test cases with clear assertions
3. Edge cases and error conditions
4. Comments explaining test rationale"""
    }

    def __init__(
        self,
        style: PromptStyle = PromptStyle.EXPERT,
        template_dir: Optional[str] = None
    ):
        """
        Initialize PromptBuilder

        Args:
            style: Default prompt style
            template_dir: Directory containing custom templates
        """
        self.style = style
        self.template_dir = Path(template_dir) if template_dir else None
        self.context: Dict[str, Any] = {}

    def set_context(self, **kwargs):
        """
        Set global context variables

        Args:
            **kwargs: Context variables
        """
        self.context.update(kwargs)

    def build(
        self,
        pattern: str,
        variables: Optional[Dict[str, Any]] = None,
        examples: Optional[List[str]] = None,
        context: Optional[str] = None,
        constraints: Optional[List[str]] = None
    ) -> str:
        """
        Build a prompt from pattern and variables

        Args:
            pattern: Pattern name or custom template
            variables: Variables to fill in template
            examples: Few-shot examples to include
            context: Additional context
            constraints: List of constraints/requirements

        Returns:
            Constructed prompt string
        """
        # Merge variables with global context
        all_vars = {**self.context, **(variables or {})}

        # Get template
        if pattern in self.PATTERNS:
            template = self.PATTERNS[pattern]
        else:
            template = pattern

        # Fill in variables
        prompt = self._fill_template(template, all_vars)

        # Add examples if provided
        if examples:
            examples_section = self._build_examples_section(examples)
            prompt = f"{prompt}\n\n{examples_section}"

        # Add context if provided
        if context:
            prompt = f"{context}\n\n{prompt}"

        # Add constraints if provided
        if constraints:
            constraints_section = self._build_constraints_section(constraints)
            prompt = f"{prompt}\n\n{constraints_section}"

        # Apply style adjustments
        prompt = self._apply_style(prompt)

        return prompt.strip()

    def build_code_generation(
        self,
        language: str,
        task: str,
        requirements: List[str],
        examples: Optional[List[Dict[str, str]]] = None,
        framework: Optional[str] = None,
        best_practices: Optional[List[str]] = None
    ) -> str:
        """
        Build a code generation prompt

        Args:
            language: Programming language
            task: Task description
            requirements: List of requirements
            examples: Example inputs/outputs
            framework: Framework to use
            best_practices: List of best practices to follow

        Returns:
            Code generation prompt
        """
        prompt = f"""Generate {language} code for the following task:

**Task**: {task}

**Requirements**:
{self._format_list(requirements)}
"""

        if framework:
            prompt += f"\n**Framework**: {framework}\n"

        if best_practices:
            prompt += f"\n**Best Practices**:\n{self._format_list(best_practices)}\n"

        if examples:
            prompt += "\n**Examples**:\n"
            for i, ex in enumerate(examples, 1):
                prompt += f"\nExample {i}:\n"
                if 'input' in ex:
                    prompt += f"Input: {ex['input']}\n"
                if 'output' in ex:
                    prompt += f"Output: {ex['output']}\n"

        prompt += f"""
Please provide:
1. Complete, production-ready code
2. Comprehensive comments explaining the logic
3. Type hints/annotations
4. Error handling
5. Example usage

Format the code with proper indentation and follow {language} conventions."""

        return prompt

    def build_refactoring_prompt(
        self,
        code: str,
        language: str,
        goals: List[str],
        preserve: Optional[List[str]] = None
    ) -> str:
        """
        Build a code refactoring prompt

        Args:
            code: Code to refactor
            language: Programming language
            goals: Refactoring goals
            preserve: Things to preserve (behavior, API, etc.)

        Returns:
            Refactoring prompt
        """
        prompt = f"""Refactor this {language} code:

```{language}
{code}
```

**Refactoring Goals**:
{self._format_list(goals)}
"""

        if preserve:
            prompt += f"\n**Preserve**:\n{self._format_list(preserve)}\n"

        prompt += """
Provide:
1. Refactored code with improvements
2. Explanation of each change
3. Before/after comparison for key improvements
4. Any trade-offs made"""

        return prompt

    def build_documentation_prompt(
        self,
        code: str,
        language: str,
        doc_style: str = "google",
        include_examples: bool = True
    ) -> str:
        """
        Build a documentation generation prompt

        Args:
            code: Code to document
            language: Programming language
            doc_style: Documentation style (google, numpy, sphinx)
            include_examples: Whether to include usage examples

        Returns:
            Documentation prompt
        """
        prompt = f"""Generate comprehensive documentation for this {language} code using {doc_style} style:

```{language}
{code}
```

Include:
1. Module/class/function docstrings
2. Parameter descriptions with types
3. Return value descriptions
4. Raises/Exceptions documentation
5. Notes about implementation details
"""

        if include_examples:
            prompt += "6. Usage examples\n"

        prompt += f"\nFollow {doc_style} documentation conventions strictly."

        return prompt

    def build_api_design_prompt(
        self,
        purpose: str,
        resources: List[str],
        authentication: str = "JWT",
        api_style: str = "REST"
    ) -> str:
        """
        Build an API design prompt

        Args:
            purpose: API purpose
            resources: List of resources/entities
            authentication: Authentication method
            api_style: API style (REST, GraphQL)

        Returns:
            API design prompt
        """
        prompt = f"""Design a {api_style} API for:

**Purpose**: {purpose}

**Resources**:
{self._format_list(resources)}

**Authentication**: {authentication}

Provide:
1. Complete API specification
2. Endpoint definitions with HTTP methods
3. Request/response schemas
4. Error handling strategy
5. Versioning approach
6. Rate limiting recommendations
7. Example requests and responses

Follow {api_style} best practices and RESTful conventions."""

        return prompt

    def build_debugging_prompt(
        self,
        code: str,
        language: str,
        error: str,
        expected: str,
        actual: str
    ) -> str:
        """
        Build a debugging assistance prompt

        Args:
            code: Code with the issue
            language: Programming language
            error: Error message
            expected: Expected behavior
            actual: Actual behavior

        Returns:
            Debugging prompt
        """
        return self.build('debug_assistant', {
            'language': language,
            'code': code,
            'error': error,
            'expected': expected,
            'actual': actual,
            'problem': f"Expected: {expected}, Got: {actual}"
        })

    def load_template(self, name: str) -> str:
        """
        Load a custom template from template directory

        Args:
            name: Template name

        Returns:
            Template content
        """
        if not self.template_dir:
            raise ValueError("Template directory not set")

        template_path = self.template_dir / f"{name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        return template_path.read_text()

    def _fill_template(self, template: str, variables: Dict[str, Any]) -> str:
        """Fill template with variables"""
        filled = template

        for key, value in variables.items():
            # Handle different value types
            if isinstance(value, list):
                value = self._format_list(value)
            elif isinstance(value, dict):
                value = self._format_dict(value)

            # Replace {key} with value
            filled = filled.replace(f"{{{key}}}", str(value))

        return filled

    def _format_list(self, items: List[str], numbered: bool = True) -> str:
        """Format list items"""
        if numbered:
            return '\n'.join(f"{i}. {item}" for i, item in enumerate(items, 1))
        else:
            return '\n'.join(f"- {item}" for item in items)

    def _format_dict(self, data: Dict[str, Any], indent: int = 0) -> str:
        """Format dictionary"""
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")

        return '\n'.join(lines)

    def _build_examples_section(self, examples: List[str]) -> str:
        """Build examples section"""
        section = "**Examples**:\n\n"
        for i, example in enumerate(examples, 1):
            section += f"Example {i}:\n{example}\n\n"
        return section

    def _build_constraints_section(self, constraints: List[str]) -> str:
        """Build constraints section"""
        return f"**Constraints**:\n{self._format_list(constraints)}"

    def _apply_style(self, prompt: str) -> str:
        """Apply style-specific modifications"""
        if self.style == PromptStyle.EXPERT:
            # Add technical depth
            if "provide:" in prompt.lower() or "include:" in prompt.lower():
                prompt += "\n\nProvide expert-level insights and advanced considerations."

        elif self.style == PromptStyle.BEGINNER:
            # Add explanatory notes
            prompt += "\n\nPlease explain concepts in simple terms with clear examples."

        elif self.style == PromptStyle.CONCISE:
            # Request brevity
            prompt += "\n\nBe concise and direct in your response."

        elif self.style == PromptStyle.DETAILED:
            # Request comprehensive coverage
            prompt += "\n\nProvide comprehensive, detailed explanations for each point."

        return prompt

    # Convenience methods for common prompts

    def code_review(self, code: str, language: str, focus: Optional[List[str]] = None) -> str:
        """Quick code review prompt"""
        variables = {'code': code, 'language': language}
        if focus:
            variables['focus'] = '\n'.join(f"- {item}" for item in focus)
        return self.build('code_review', variables)

    def optimize_code(self, code: str, language: str, goal: str) -> str:
        """Quick optimization prompt"""
        return self.build('optimization', {
            'code': code,
            'language': language,
            'goal': goal,
            'requirements': 'Maintain functionality while improving ' + goal
        })

    def generate_tests(
        self,
        code: str,
        language: str,
        framework: str,
        coverage: int = 80
    ) -> str:
        """Quick test generation prompt"""
        return self.build('test_generation', {
            'code': code,
            'language': language,
            'framework': framework,
            'coverage': coverage
        })

    def design_architecture(
        self,
        system_name: str,
        purpose: str,
        requirements: List[str],
        scale: str = "medium"
    ) -> str:
        """Quick architecture design prompt"""
        return self.build('architecture_design', {
            'system_name': system_name,
            'purpose': purpose,
            'requirements': self._format_list(requirements),
            'scale': scale,
            'constraints': 'Standard cloud infrastructure'
        })


# Convenience function
def quick_prompt(pattern: str, **kwargs) -> str:
    """
    Quickly build a prompt

    Args:
        pattern: Pattern name
        **kwargs: Variables

    Returns:
        Built prompt
    """
    builder = PromptBuilder()
    return builder.build(pattern, kwargs)
