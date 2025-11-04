"""
File Manager Utility
Handles all file operations with templates, safety checks, and utilities
"""

import os
import shutil
import json
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import hashlib
import time


class FileManager:
    """
    Comprehensive file management utility for ByteClaude framework
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize FileManager

        Args:
            base_path: Base directory for operations (defaults to current directory)
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.created_files: List[Path] = []
        self.created_dirs: List[Path] = []

    # Directory Operations

    def create_directory(self, path: Union[str, Path], exist_ok: bool = True) -> Path:
        """
        Create a directory with proper error handling

        Args:
            path: Directory path to create
            exist_ok: Whether to ignore if directory exists

        Returns:
            Path object of created directory
        """
        dir_path = self._resolve_path(path)
        dir_path.mkdir(parents=True, exist_ok=exist_ok)
        self.created_dirs.append(dir_path)
        return dir_path

    def create_directory_structure(self, structure: Dict[str, Any], base_path: Optional[Path] = None) -> List[Path]:
        """
        Create nested directory structure from dictionary

        Args:
            structure: Nested dict representing directory structure
            base_path: Base path for structure (defaults to self.base_path)

        Returns:
            List of created directory paths
        """
        created = []
        base = base_path or self.base_path

        for name, content in structure.items():
            path = base / name
            if isinstance(content, dict):
                # Nested directory
                self.create_directory(path)
                created.append(path)
                created.extend(self.create_directory_structure(content, path))
            else:
                # File or empty directory
                if content is None:
                    self.create_directory(path)
                    created.append(path)

        return created

    def list_directory(
        self,
        path: Union[str, Path],
        pattern: Optional[str] = None,
        recursive: bool = False
    ) -> List[Path]:
        """
        List directory contents with optional filtering

        Args:
            path: Directory to list
            pattern: Glob pattern to filter (e.g., "*.py")
            recursive: Whether to search recursively

        Returns:
            List of matching paths
        """
        dir_path = self._resolve_path(path)

        if not dir_path.is_dir():
            raise NotADirectoryError(f"{dir_path} is not a directory")

        if pattern:
            if recursive:
                return list(dir_path.rglob(pattern))
            else:
                return list(dir_path.glob(pattern))
        else:
            return list(dir_path.iterdir())

    # File Operations

    def create_file(
        self,
        path: Union[str, Path],
        content: str = "",
        overwrite: bool = False
    ) -> Path:
        """
        Create a file with content

        Args:
            path: File path to create
            content: Content to write
            overwrite: Whether to overwrite existing file

        Returns:
            Path object of created file
        """
        file_path = self._resolve_path(path)

        if file_path.exists() and not overwrite:
            raise FileExistsError(f"{file_path} already exists")

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding='utf-8')
        self.created_files.append(file_path)
        return file_path

    def read_file(self, path: Union[str, Path]) -> str:
        """
        Read file content as text

        Args:
            path: File path to read

        Returns:
            File content as string
        """
        file_path = self._resolve_path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist")

        return file_path.read_text(encoding='utf-8')

    def write_file(
        self,
        path: Union[str, Path],
        content: str,
        append: bool = False
    ) -> Path:
        """
        Write content to file

        Args:
            path: File path to write
            content: Content to write
            append: Whether to append to existing content

        Returns:
            Path object of written file
        """
        file_path = self._resolve_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if append:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
        else:
            file_path.write_text(content, encoding='utf-8')

        if file_path not in self.created_files:
            self.created_files.append(file_path)

        return file_path

    def copy_file(self, src: Union[str, Path], dst: Union[str, Path]) -> Path:
        """
        Copy file from source to destination

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            Path object of destination file
        """
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)

        if not src_path.exists():
            raise FileNotFoundError(f"{src_path} does not exist")

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        self.created_files.append(dst_path)
        return dst_path

    def move_file(self, src: Union[str, Path], dst: Union[str, Path]) -> Path:
        """
        Move file from source to destination

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            Path object of destination file
        """
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)

        if not src_path.exists():
            raise FileNotFoundError(f"{src_path} does not exist")

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        return dst_path

    def delete_file(self, path: Union[str, Path]) -> None:
        """
        Delete a file

        Args:
            path: File path to delete
        """
        file_path = self._resolve_path(path)

        if file_path.exists():
            file_path.unlink()

    def delete_directory(self, path: Union[str, Path], recursive: bool = False) -> None:
        """
        Delete a directory

        Args:
            path: Directory path to delete
            recursive: Whether to delete recursively
        """
        dir_path = self._resolve_path(path)

        if dir_path.exists():
            if recursive:
                shutil.rmtree(dir_path)
            else:
                dir_path.rmdir()

    # JSON Operations

    def read_json(self, path: Union[str, Path]) -> Any:
        """
        Read JSON file

        Args:
            path: JSON file path

        Returns:
            Parsed JSON data
        """
        content = self.read_file(path)
        return json.loads(content)

    def write_json(
        self,
        path: Union[str, Path],
        data: Any,
        indent: int = 2
    ) -> Path:
        """
        Write data to JSON file

        Args:
            path: JSON file path
            data: Data to write
            indent: JSON indentation

        Returns:
            Path object of written file
        """
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        return self.write_file(path, content)

    # YAML Operations

    def read_yaml(self, path: Union[str, Path]) -> Any:
        """
        Read YAML file

        Args:
            path: YAML file path

        Returns:
            Parsed YAML data
        """
        content = self.read_file(path)
        return yaml.safe_load(content)

    def write_yaml(self, path: Union[str, Path], data: Any) -> Path:
        """
        Write data to YAML file

        Args:
            path: YAML file path
            data: Data to write

        Returns:
            Path object of written file
        """
        content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        return self.write_file(path, content)

    # File Information

    def get_file_info(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get detailed file information

        Args:
            path: File path

        Returns:
            Dictionary with file information
        """
        file_path = self._resolve_path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist")

        stat = file_path.stat()

        return {
            'name': file_path.name,
            'path': str(file_path.absolute()),
            'size': stat.st_size,
            'size_human': self._human_readable_size(stat.st_size),
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_file': file_path.is_file(),
            'is_directory': file_path.is_dir(),
            'extension': file_path.suffix,
            'checksum': self._calculate_checksum(file_path) if file_path.is_file() else None
        }

    def file_exists(self, path: Union[str, Path]) -> bool:
        """
        Check if file exists

        Args:
            path: File path

        Returns:
            True if file exists
        """
        return self._resolve_path(path).exists()

    def get_file_size(self, path: Union[str, Path]) -> int:
        """
        Get file size in bytes

        Args:
            path: File path

        Returns:
            File size in bytes
        """
        file_path = self._resolve_path(path)
        return file_path.stat().st_size if file_path.exists() else 0

    # Template Operations

    def create_from_template(
        self,
        template_path: Union[str, Path],
        output_path: Union[str, Path],
        variables: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Create file from template with variable substitution

        Args:
            template_path: Path to template file
            output_path: Path for output file
            variables: Variables for substitution

        Returns:
            Path object of created file
        """
        template_content = self.read_file(template_path)

        if variables:
            # Simple variable substitution
            for key, value in variables.items():
                template_content = template_content.replace(f"{{{{{key}}}}}", str(value))

        return self.create_file(output_path, template_content, overwrite=True)

    # Bulk Operations

    def copy_directory(
        self,
        src: Union[str, Path],
        dst: Union[str, Path],
        ignore_patterns: Optional[List[str]] = None
    ) -> Path:
        """
        Copy entire directory

        Args:
            src: Source directory
            dst: Destination directory
            ignore_patterns: Patterns to ignore (e.g., ["*.pyc", "__pycache__"])

        Returns:
            Path object of destination directory
        """
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)

        if not src_path.is_dir():
            raise NotADirectoryError(f"{src_path} is not a directory")

        ignore_func = None
        if ignore_patterns:
            ignore_func = shutil.ignore_patterns(*ignore_patterns)

        shutil.copytree(src_path, dst_path, ignore=ignore_func, dirs_exist_ok=True)
        self.created_dirs.append(dst_path)
        return dst_path

    def cleanup_created_files(self) -> None:
        """
        Delete all files and directories created by this FileManager instance
        """
        # Delete files first
        for file_path in reversed(self.created_files):
            if file_path.exists():
                file_path.unlink()

        # Then delete directories
        for dir_path in reversed(self.created_dirs):
            if dir_path.exists() and not any(dir_path.iterdir()):
                dir_path.rmdir()

        self.created_files.clear()
        self.created_dirs.clear()

    # Search Operations

    def find_files(
        self,
        path: Union[str, Path],
        name_pattern: Optional[str] = None,
        content_pattern: Optional[str] = None,
        extensions: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Find files by name pattern, content, or extension

        Args:
            path: Directory to search
            name_pattern: File name glob pattern
            content_pattern: Content to search for
            extensions: List of file extensions to include

        Returns:
            List of matching file paths
        """
        results = []
        search_path = self._resolve_path(path)

        # Get all files
        if name_pattern:
            files = list(search_path.rglob(name_pattern))
        else:
            files = [p for p in search_path.rglob("*") if p.is_file()]

        # Filter by extension
        if extensions:
            files = [f for f in files if f.suffix in extensions]

        # Filter by content
        if content_pattern:
            for file_path in files:
                try:
                    content = self.read_file(file_path)
                    if content_pattern in content:
                        results.append(file_path)
                except (UnicodeDecodeError, PermissionError):
                    continue
        else:
            results = files

        return results

    # Helper Methods

    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """
        Resolve path relative to base_path

        Args:
            path: Path to resolve

        Returns:
            Resolved absolute Path object
        """
        path_obj = Path(path)

        if path_obj.is_absolute():
            return path_obj
        else:
            return (self.base_path / path_obj).resolve()

    def _human_readable_size(self, size: int) -> str:
        """
        Convert bytes to human readable format

        Args:
            size: Size in bytes

        Returns:
            Human readable size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def _calculate_checksum(self, path: Path, algorithm: str = 'sha256') -> str:
        """
        Calculate file checksum

        Args:
            path: File path
            algorithm: Hash algorithm (md5, sha256, etc.)

        Returns:
            Hexadecimal checksum string
        """
        hash_obj = hashlib.new(algorithm)

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Optionally cleanup on error
        if exc_type is not None:
            self.cleanup_created_files()
        return False
