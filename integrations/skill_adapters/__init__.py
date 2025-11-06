"""
Skill Adapters Package
Adapters for integrating with ByteClaude skills
"""

__version__ = "1.0.0"

from .document_skills import DocumentSkillsAdapter
from .web_skills import WebSkillsAdapter
from .design_skills import DesignSkillsAdapter
from .dev_skills import DevSkillsAdapter
from .stripe_skills import StripeSkillsAdapter

__all__ = [
    'DocumentSkillsAdapter',
    'WebSkillsAdapter',
    'DesignSkillsAdapter',
    'DevSkillsAdapter',
    'StripeSkillsAdapter'
]
