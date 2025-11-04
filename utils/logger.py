"""
Logging Utility
Structured logging with context and formatting for ByteClaude framework
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json


class ContextLogger(logging.Logger):
    """
    Enhanced logger with context support
    """

    def __init__(self, name: str, level=logging.NOTSET):
        super().__init__(name, level)
        self.context: Dict[str, Any] = {}

    def set_context(self, **kwargs):
        """Add context to logger"""
        self.context.update(kwargs)

    def clear_context(self):
        """Clear all context"""
        self.context.clear()

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """Override _log to include context"""
        if extra is None:
            extra = {}

        extra['context'] = self.context.copy()
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel + 1)


class ColoredFormatter(logging.Formatter):
    """
    Colored log formatter for console output
    """

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        """Format log record with colors"""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            record.msg = f"{self.COLORS[levelname]}{record.msg}{self.COLORS['RESET']}"

        return super().format(record)


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    """

    def format(self, record):
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add context if available
        if hasattr(record, 'context') and record.context:
            log_data['context'] = record.context

        # Add exception info if available
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, default=str)


def setup_logger(
    name: str = "byteclaude",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: str = "./logs",
    use_colors: bool = True,
    json_format: bool = False
) -> ContextLogger:
    """
    Setup and configure a logger

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log file name (optional)
        log_dir: Directory for log files
        use_colors: Whether to use colored output for console
        json_format: Whether to use JSON formatting

    Returns:
        Configured ContextLogger instance
    """
    # Register custom logger class
    logging.setLoggerClass(ContextLogger)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    if json_format:
        console_formatter = JSONFormatter()
    elif use_colors:
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path / log_file)
        file_handler.setLevel(logging.DEBUG)  # Log everything to file

        if json_format:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "byteclaude") -> ContextLogger:
    """
    Get or create a logger

    Args:
        name: Logger name

    Returns:
        ContextLogger instance
    """
    logging.setLoggerClass(ContextLogger)
    return logging.getLogger(name)


class LoggerContext:
    """
    Context manager for temporary logger context
    """

    def __init__(self, logger: ContextLogger, **context):
        """
        Initialize logger context

        Args:
            logger: Logger to add context to
            **context: Context key-value pairs
        """
        self.logger = logger
        self.context = context
        self.old_context = {}

    def __enter__(self):
        """Enter context"""
        self.old_context = self.logger.context.copy()
        self.logger.set_context(**self.context)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        self.logger.context = self.old_context
        return False


# Pre-configured loggers for different components
def get_task_logger() -> ContextLogger:
    """Get logger for task planning"""
    return get_logger("byteclaude.task_planner")


def get_execution_logger() -> ContextLogger:
    """Get logger for execution engine"""
    return get_logger("byteclaude.execution")


def get_integration_logger() -> ContextLogger:
    """Get logger for integrations"""
    return get_logger("byteclaude.integration")


def get_skill_logger() -> ContextLogger:
    """Get logger for skills"""
    return get_logger("byteclaude.skill")


def get_mcp_logger() -> ContextLogger:
    """Get logger for MCPs"""
    return get_logger("byteclaude.mcp")


# Convenience decorators
def log_execution(logger: Optional[ContextLogger] = None):
    """
    Decorator to log function execution

    Args:
        logger: Logger to use (defaults to root logger)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_logger()

            func_name = func.__name__
            logger.debug(f"Entering {func_name}")

            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func_name} successfully")
                return result
            except Exception as e:
                logger.error(f"Error in {func_name}: {str(e)}", exc_info=True)
                raise

        return wrapper
    return decorator


def log_performance(logger: Optional[ContextLogger] = None):
    """
    Decorator to log function performance

    Args:
        logger: Logger to use (defaults to root logger)
    """
    import time

    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_logger()

            func_name = func.__name__
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{func_name} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{func_name} failed after {duration:.2f}s: {str(e)}")
                raise

        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Setup logger
    logger = setup_logger(
        name="test",
        level="DEBUG",
        log_file="test.log",
        use_colors=True
    )

    # Basic logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # With context
    logger.set_context(task_id="task_123", user="alice")
    logger.info("Processing task")

    # Using context manager
    with LoggerContext(logger, phase="validation", step=1):
        logger.info("Validating input")

    # Using decorators
    @log_execution(logger)
    @log_performance(logger)
    def example_function():
        import time
        time.sleep(0.1)
        return "done"

    example_function()
