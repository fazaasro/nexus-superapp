#!/usr/bin/env python3
"""
Test script for The Brain module (Knowledge Management).
Tests knowledge entry CRUD, search, and statistics.
"""
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.brain.service import BrainModule
from core.database import init_db


def test_brain_module():
    """Test Brain module functionality."""
    print("\n" + "="*70)
    print("NEXUS BRAIN MODULE - KNOWLEDGE MANAGEMENT TESTS")
    print("="*70)

    # Initialize database
    print("\n[1/8] Initializing database...")
    init_db()
    print("✅ Database initialized")

    brain = BrainModule()
    user_id = 'faza'

    # Test 1: Create knowledge entry
    print("\n[2/8] Creating knowledge entry...")
    entry_data = {
        'title': 'Docker container networking basics',
        'content': """Q: What is the default network mode for Docker containers?
A: Bridge mode. Each container gets its own IP address and can communicate
   with other containers on the same bridge network.

Docker networking modes:
1. Bridge - Default, container-to-container on same host
2. Host - Container shares host's network stack
3. Overlay - Multi-host networking
4. None - No networking

To connect containers: docker network connect <network> <container>""",
        'content_type': 'note',
        'domain': 'tech',
        'project': 'aac-infrastructure',
        'tags': ['docker', 'networking', 'containers'],
        'is_srs_eligible': True
    }
    
    result = brain.create_entry(entry_data, user_id)
    assert 'id' in result, f"Failed to create entry: {result}"
    assert result['status'] == 'created', f"Unexpected status: {result}"
    entry_id = result['id']
    print(f"✅ Entry created: {entry_id}")

    # Test 2: Get single entry
    print("\n[3/8] Retrieving single entry...")
    entry = brain.get_entry(entry_id, user_id)
    assert entry is not None, "Entry not found"
    assert entry['title'] == entry_data['title'], f"Title mismatch: {entry['title']}"
    assert entry['domain'] == 'tech', f"Domain mismatch: {entry['domain']}"
    assert 'docker' in entry['tags'], f"Tags missing: {entry['tags']}"
    print(f"✅ Entry retrieved: {entry['title']}")

    # Test 3: List entries
    print("\n[4/8] Listing entries...")
    entries = brain.get_entries(user_id)
    assert len(entries) > 0, "No entries found"
    print(f"✅ Found {len(entries)} entries")

    # Test 4: Update entry
    print("\n[5/8] Updating entry...")
    update_data = {
        'tags': ['docker', 'networking', 'containers', 'updated'],
        'domain': 'tech'
    }
    result = brain.update_entry(entry_id, update_data, user_id)
    assert result['status'] == 'updated', f"Failed to update: {result}"
    
    # Verify update
    updated_entry = brain.get_entry(entry_id, user_id)
    assert 'updated' in updated_entry['tags'], "Tag not updated"
    print(f"✅ Entry updated: {updated_entry['tags']}")

    # Test 5: Search entries
    print("\n[6/8] Searching entries...")
    results = brain.search_entries('docker networking', user_id)
    assert len(results) > 0, f"No results found for search"
    assert results[0]['id'] == entry_id, f"Wrong entry in search results"
    print(f"✅ Search returned {len(results)} results")

    # Test 6: Filter by domain
    print("\n[7/8] Filtering by domain...")
    tech_entries = brain.get_entries(user_id, domain='tech')
    assert len(tech_entries) > 0, "No tech entries found"
    assert all(e['domain'] == 'tech' for e in tech_entries), "Domain filter failed"
    print(f"✅ Found {len(tech_entries)} tech entries")

    # Test 7: Create Anki card (placeholder)
    print("\n[8/8] Creating Anki card...")
    result = brain.create_anki_card(entry_id, user_id)
    assert 'anki_card_id' in result, f"Failed to create Anki card: {result}"
    print(f"✅ Anki card created: {result['anki_card_id']}")

    # Test 8: Get statistics
    print("\n[9/9] Getting statistics...")
    stats = brain.get_stats(user_id)
    assert 'total_entries' in stats, "Stats missing total_entries"
    assert 'entries_by_domain' in stats, "Stats missing entries_by_domain"
    print(f"✅ Statistics: {stats['total_entries']} total entries")
    print(f"   By domain: {stats['entries_by_domain']}")

    # Summary
    print("\n" + "="*70)
    print("ALL BRAIN MODULE TESTS PASSED ✅")
    print("="*70)
    print(f"\nTest entry ID: {entry_id}")
    print(f"Created {stats['total_entries']} knowledge entries")
    print("\nNext steps:")
    print("1. Implement Qdrant integration for vector embeddings")
    print("2. Implement AnkiConnect integration for card sync")
    print("3. Implement web content extraction for clipping")
    print("4. Implement knowledge graph for connections")


def test_worktrees():
    """Test worktree management."""
    print("\n" + "="*70)
    print("NEXUS BRAIN MODULE - WORKTREE MANAGEMENT TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    brain = BrainModule()
    user_id = 'faza'

    # Test 1: Create worktree
    print("\n[1/3] Creating worktree...")
    worktree_data = {
        'repo_name': 'aac-infrastructure',
        'branch_name': 'feature/docker-networking',
        'worktree_path': '/home/ai-dev/swarm/repos/aac-infrastructure-docker',
        'context_notes': 'Testing new Docker networking configuration'
    }
    
    result = brain.create_worktree(worktree_data, user_id)
    assert 'id' in result, f"Failed to create worktree: {result}"
    worktree_id = result['id']
    print(f"✅ Worktree created: {worktree_id}")

    # Test 2: List worktrees
    print("\n[2/3] Listing worktrees...")
    worktrees = brain.get_worktrees(user_id)
    assert len(worktrees) > 0, "No worktrees found"
    assert worktrees[0]['branch_name'] == worktree_data['branch_name'], "Worktree data mismatch"
    print(f"✅ Found {len(worktrees)} worktrees")

    # Test 3: Update access
    print("\n[3/3] Updating worktree access...")
    result = brain.update_worktree_access(worktree_id, user_id)
    assert result['status'] == 'accessed', f"Failed to update access: {result}"
    print(f"✅ Worktree access updated")

    print("\n" + "="*70)
    print("ALL WORKTREE TESTS PASSED ✅")
    print("="*70)


if __name__ == '__main__':
    try:
        test_brain_module()
        test_worktrees()
        print("\n✅ All tests passed successfully!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
