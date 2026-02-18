"""
Models for The Brain module (using dataclasses - no pydantic dependency)
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class KnowledgeEntryCreate:
    """Create a new knowledge entry"""
    title: str
    content: str
    content_type: str = "note"  # note, voice_transcript, web_clip, code, pdf_extract
    domain: Optional[str] = None  # tech, dnd, masters, life, finance, health
    project: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)
    source_url: Optional[str] = None
    source_file: Optional[str] = None
    is_srs_eligible: bool = False  # Eligible for spaced repetition


@dataclass
class KnowledgeEntryUpdate:
    """Update a knowledge entry"""
    title: Optional[str] = None
    content: Optional[str] = None
    domain: Optional[str] = None
    project: Optional[str] = None
    tags: Optional[List[str]] = None
    is_srs_eligible: Optional[bool] = None


@dataclass
class AnkiCardCreate:
    """Create an Anki card"""
    deck: str
    front: str
    back: str
    tags: Optional[List[str]] = field(default_factory=list)
    model: str = "Basic"  # Anki card model (Basic, Cloze, etc.)


@dataclass
class WorktreeCreate:
    """Create a git worktree entry"""
    repo_name: str
    branch_name: str
    worktree_path: str
    context_notes: Optional[str] = None


@dataclass
class ConnectionCreate:
    """Connect knowledge entries"""
    entry_id: str
    related_ids: List[str]
    relationship_type: str = "related"  # related, prerequisite, followup, conflict


@dataclass
class SearchQuery:
    """Search query for semantic search"""
    query: str
    domain: Optional[str] = None
    owner: Optional[str] = None
    project: Optional[str] = None
    limit: int = 10
    score_threshold: float = 0.5


@dataclass
class WebClipRequest:
    """Request to clip a web page"""
    url: str
    domain: Optional[str] = "tech"
    title: Optional[str] = None  # Auto-extracted if not provided
    project: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)
