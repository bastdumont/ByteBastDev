"""
Context7 Client
Integration with Context7 for fetching library documentation
"""

import time
from typing import Optional, Dict, Any, List
from pathlib import Path
import yaml
import hashlib
import json


class Context7Client:
    """
    Client for Context7 documentation retrieval service
    """

    def __init__(
        self,
        cache_enabled: bool = True,
        cache_ttl: int = 3600,
        cache_dir: str = "./cache/context7",
        mappings_file: Optional[str] = None
    ):
        """
        Initialize Context7Client

        Args:
            cache_enabled: Whether to cache documentation
            cache_ttl: Cache time-to-live in seconds
            cache_dir: Directory for cache files
            mappings_file: Path to library mappings YAML file
        """
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self.cache_dir = Path(cache_dir)

        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load library mappings
        self.library_mappings = self._load_mappings(mappings_file)

        # Cache metadata
        self.cache_metadata: Dict[str, Dict[str, Any]] = {}
        self._load_cache_metadata()

    def resolve_library_id(self, library_name: str) -> Optional[str]:
        """
        Resolve library name to Context7-compatible library ID

        Args:
            library_name: Library name (e.g., "react", "next.js")

        Returns:
            Context7 library ID (e.g., "/facebook/react") or None
        """
        library_lower = library_name.lower()

        # Direct search in all categories
        for category_data in self.library_mappings.values():
            if not isinstance(category_data, dict):
                continue

            for lib_key, lib_info in category_data.items():
                if not isinstance(lib_info, dict):
                    continue

                # Check direct match
                if lib_key.lower() == library_lower:
                    return lib_info.get('context7_id')

                # Check aliases
                aliases = lib_info.get('aliases', [])
                if library_lower in [a.lower() for a in aliases]:
                    return lib_info.get('context7_id')

        return None

    def get_library_docs(
        self,
        library_name: str,
        topic: Optional[str] = None,
        tokens: int = 10000,
        force_refresh: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Get documentation for a library

        Args:
            library_name: Library name
            topic: Specific topic to focus on
            tokens: Maximum tokens to retrieve
            force_refresh: Whether to bypass cache

        Returns:
            Documentation data or None
        """
        # Resolve library ID
        library_id = self.resolve_library_id(library_name)

        if not library_id:
            return {
                'error': 'library_not_found',
                'message': f"Could not resolve library: {library_name}",
                'library_name': library_name
            }

        # Check cache
        if self.cache_enabled and not force_refresh:
            cached = self._get_from_cache(library_id, topic)
            if cached:
                return cached

        # In a real implementation, this would make an API call to Context7
        # For now, we simulate the response structure
        docs = self._fetch_documentation(library_id, topic, tokens)

        # Cache the result
        if self.cache_enabled and docs:
            self._save_to_cache(library_id, topic, docs)

        return docs

    def get_multiple_libraries(
        self,
        libraries: List[str],
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get documentation for multiple libraries

        Args:
            libraries: List of library names
            topic: Topic to focus on (applies to all)

        Returns:
            Dictionary mapping library names to their docs
        """
        results = {}

        for lib in libraries:
            docs = self.get_library_docs(lib, topic)
            results[lib] = docs

        return results

    def get_library_info(self, library_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a library

        Args:
            library_name: Library name

        Returns:
            Library information
        """
        library_lower = library_name.lower()

        for category_name, category_data in self.library_mappings.items():
            if not isinstance(category_data, dict):
                continue

            for lib_key, lib_info in category_data.items():
                if not isinstance(lib_info, dict):
                    continue

                if lib_key.lower() == library_lower:
                    return {
                        'name': lib_key,
                        'category': category_name,
                        'context7_id': lib_info.get('context7_id'),
                        'aliases': lib_info.get('aliases', []),
                        'topics': lib_info.get('topics', [])
                    }

        return None

    def search_libraries(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for libraries

        Args:
            query: Search query
            category: Filter by category

        Returns:
            List of matching libraries
        """
        results = []
        query_lower = query.lower()

        for category_name, category_data in self.library_mappings.items():
            if category and category != category_name:
                continue

            if not isinstance(category_data, dict):
                continue

            for lib_key, lib_info in category_data.items():
                if not isinstance(lib_info, dict):
                    continue

                # Check if query matches library name or aliases
                if query_lower in lib_key.lower():
                    results.append({
                        'name': lib_key,
                        'category': category_name,
                        'context7_id': lib_info.get('context7_id'),
                        'relevance': 1.0
                    })
                    continue

                aliases = lib_info.get('aliases', [])
                if any(query_lower in alias.lower() for alias in aliases):
                    results.append({
                        'name': lib_key,
                        'category': category_name,
                        'context7_id': lib_info.get('context7_id'),
                        'relevance': 0.8
                    })

        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results

    def clear_cache(self, library_name: Optional[str] = None) -> None:
        """
        Clear documentation cache

        Args:
            library_name: Specific library to clear (None = clear all)
        """
        if not self.cache_enabled:
            return

        if library_name:
            library_id = self.resolve_library_id(library_name)
            if library_id:
                cache_key = self._get_cache_key(library_id, None)
                cache_file = self.cache_dir / f"{cache_key}.json"
                if cache_file.exists():
                    cache_file.unlink()
        else:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()

        self.cache_metadata.clear()
        self._save_cache_metadata()

    def _load_mappings(self, mappings_file: Optional[str]) -> Dict[str, Any]:
        """Load library mappings from file"""
        if mappings_file:
            path = Path(mappings_file)
        else:
            # Default location
            path = Path("config/context7-library-mappings.yaml")

        if not path.exists():
            return {}

        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}

    def _fetch_documentation(
        self,
        library_id: str,
        topic: Optional[str],
        tokens: int
    ) -> Dict[str, Any]:
        """
        Fetch documentation from Context7

        In a real implementation, this would make an API call.
        For now, returns simulated structure.
        """
        # Simulated documentation structure
        return {
            'library_id': library_id,
            'topic': topic,
            'tokens': tokens,
            'documentation': f"""
# {library_id} Documentation

{f'Topic: {topic}' if topic else 'General Documentation'}

This would contain the actual documentation content from Context7.
Including:
- Getting started guides
- API reference
- Best practices
- Code examples
- Common patterns

Retrieved: {time.strftime('%Y-%m-%d %H:%M:%S')}
Tokens: {tokens}
""",
            'metadata': {
                'fetched_at': time.time(),
                'source': 'context7',
                'version': 'latest'
            }
        }

    def _get_cache_key(self, library_id: str, topic: Optional[str]) -> str:
        """Generate cache key"""
        key_str = f"{library_id}:{topic or 'general'}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(
        self,
        library_id: str,
        topic: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Get documentation from cache"""
        cache_key = self._get_cache_key(library_id, topic)

        # Check if cache exists and is valid
        if cache_key in self.cache_metadata:
            cached_time = self.cache_metadata[cache_key]['cached_at']
            if time.time() - cached_time < self.cache_ttl:
                cache_file = self.cache_dir / f"{cache_key}.json"
                if cache_file.exists():
                    with open(cache_file, 'r') as f:
                        return json.load(f)

        return None

    def _save_to_cache(
        self,
        library_id: str,
        topic: Optional[str],
        docs: Dict[str, Any]
    ) -> None:
        """Save documentation to cache"""
        cache_key = self._get_cache_key(library_id, topic)
        cache_file = self.cache_dir / f"{cache_key}.json"

        with open(cache_file, 'w') as f:
            json.dump(docs, f, indent=2)

        self.cache_metadata[cache_key] = {
            'library_id': library_id,
            'topic': topic,
            'cached_at': time.time()
        }
        self._save_cache_metadata()

    def _load_cache_metadata(self) -> None:
        """Load cache metadata"""
        metadata_file = self.cache_dir / "cache_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                self.cache_metadata = json.load(f)

    def _save_cache_metadata(self) -> None:
        """Save cache metadata"""
        metadata_file = self.cache_dir / "cache_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.cache_metadata, f, indent=2)

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_cached = len(self.cache_metadata)
        expired = 0
        valid = 0

        current_time = time.time()
        for metadata in self.cache_metadata.values():
            if current_time - metadata['cached_at'] >= self.cache_ttl:
                expired += 1
            else:
                valid += 1

        return {
            'total_entries': total_cached,
            'valid_entries': valid,
            'expired_entries': expired,
            'cache_ttl': self.cache_ttl,
            'cache_enabled': self.cache_enabled
        }
