"""
Filesystem MCP Handler
Complete file system operations
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import os
import shutil


class FilesystemHandler:
    """
    Handler for Filesystem MCP operations
    Provides file and directory management
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Filesystem handler"""
        self.config = config
        self.allowed_paths = config.get('allowed_paths', [])
        self.base_path = Path(config.get('base_path', '.'))

    async def read_file(self, path: str) -> Dict[str, Any]:
        """Read file content"""
        file_path = self.base_path / path

        if not self._is_allowed(file_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            content = file_path.read_text(encoding='utf-8')
            return {'success': True, 'content': content, 'path': str(file_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write file content"""
        file_path = self.base_path / path

        if not self._is_allowed(file_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return {'success': True, 'path': str(file_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def list_directory(self, path: str = '.') -> Dict[str, Any]:
        """List directory contents"""
        dir_path = self.base_path / path

        if not self._is_allowed(dir_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            entries = []
            for item in dir_path.iterdir():
                entries.append({
                    'name': item.name,
                    'path': str(item),
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else None
                })
            return {'success': True, 'entries': entries}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def create_directory(self, path: str) -> Dict[str, Any]:
        """Create directory"""
        dir_path = self.base_path / path

        if not self._is_allowed(dir_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return {'success': True, 'path': str(dir_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def delete_file(self, path: str) -> Dict[str, Any]:
        """Delete file"""
        file_path = self.base_path / path

        if not self._is_allowed(file_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            file_path.unlink()
            return {'success': True, 'path': str(file_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move file"""
        src_path = self.base_path / source
        dst_path = self.base_path / destination

        if not (self._is_allowed(src_path) and self._is_allowed(dst_path)):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            shutil.move(str(src_path), str(dst_path))
            return {'success': True, 'from': str(src_path), 'to': str(dst_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Copy file"""
        src_path = self.base_path / source
        dst_path = self.base_path / destination

        if not (self._is_allowed(src_path) and self._is_allowed(dst_path)):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            shutil.copy2(src_path, dst_path)
            return {'success': True, 'from': str(src_path), 'to': str(dst_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def get_file_info(self, path: str) -> Dict[str, Any]:
        """Get file information"""
        file_path = self.base_path / path

        if not self._is_allowed(file_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            stat = file_path.stat()
            return {
                'success': True,
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def search_files(
        self,
        pattern: str,
        path: str = '.',
        recursive: bool = True
    ) -> Dict[str, Any]:
        """Search for files by pattern"""
        search_path = self.base_path / path

        if not self._is_allowed(search_path):
            return {'success': False, 'error': 'Path not allowed'}

        try:
            if recursive:
                matches = list(search_path.rglob(pattern))
            else:
                matches = list(search_path.glob(pattern))

            results = [str(m) for m in matches]
            return {'success': True, 'matches': results, 'count': len(results)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _is_allowed(self, path: Path) -> bool:
        """Check if path is allowed"""
        if not self.allowed_paths:
            return True

        path_str = str(path.resolve())
        return any(path_str.startswith(str(allowed)) for allowed in self.allowed_paths)
