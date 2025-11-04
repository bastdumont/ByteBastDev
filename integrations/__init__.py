"""
ByteClaude Integrations Package
External service integrations (Context7, MCPs, Skills)
"""

__version__ = "1.0.0"

from .context7_client import Context7Client

# MCP Handlers
from .mcp_handlers.mongodb_handler import MongoDBHandler
from .mcp_handlers.stripe_handler import StripeHandler
from .mcp_handlers.notion_handler import NotionHandler
from .mcp_handlers.airtable_handler import AirtableHandler
from .mcp_handlers.hubspot_handler import HubSpotHandler
from .mcp_handlers.filesystem_handler import FilesystemHandler
from .mcp_handlers.chrome_handler import ChromeHandler
from .mcp_handlers.web_tools_handler import WebToolsHandler

# Skill Adapters
from .skill_adapters.document_skills import DocumentSkillsAdapter
from .skill_adapters.web_skills import WebSkillsAdapter
from .skill_adapters.design_skills import DesignSkillsAdapter
from .skill_adapters.dev_skills import DevSkillsAdapter

__all__ = [
    # Context7
    'Context7Client',

    # MCP Handlers
    'MongoDBHandler',
    'StripeHandler',
    'NotionHandler',
    'AirtableHandler',
    'HubSpotHandler',
    'FilesystemHandler',
    'ChromeHandler',
    'WebToolsHandler',

    # Skill Adapters
    'DocumentSkillsAdapter',
    'WebSkillsAdapter',
    'DesignSkillsAdapter',
    'DevSkillsAdapter'
]
