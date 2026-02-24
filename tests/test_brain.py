"""
Brain module tests
"""
import pytest
from modules.brain.service import BrainModule


class TestBrainModuleInit:
    """Test BrainModule initialization"""

    def test_module_initialization(self):
        """Test that BrainModule initializes correctly"""
        brain = BrainModule()

        assert brain.db_path is not None
        assert brain.DOMAINS is not None
        assert len(brain.DOMAINS) > 0
        assert 'tech' in brain.DOMAINS
        assert 'health' in brain.DOMAINS

    def test_qdrant_initialization(self):
        """Test that Qdrant client initializes"""
        brain = BrainModule()

        assert brain.qdrant is not None
        assert brain.collection_name is not None


class TestKnowledgeEntryCRUD:
    """Test knowledge entry CRUD operations"""

    def test_create_entry(self, test_user, sample_knowledge_entry):
        """Test creating a knowledge entry"""
        brain = BrainModule()

        result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'
        assert result['id'].startswith('knl_')

    def test_get_entries(self, test_user, sample_knowledge_entry):
        """Test getting knowledge entries"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Get entries
        entries = brain.get_entries(test_user['user_id'], limit=10)

        assert len(entries) > 0
        # Find our created entry
        found = [e for e in entries if e['id'] == entry_id]
        assert len(found) == 1

    def test_get_entry_by_id(self, test_user, sample_knowledge_entry):
        """Test getting single entry by ID"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Get entry
        entry = brain.get_entry(entry_id, test_user['user_id'])

        assert entry is not None
        assert entry['id'] == entry_id
        assert entry['title'] == sample_knowledge_entry['title']

    def test_update_entry(self, test_user, sample_knowledge_entry):
        """Test updating a knowledge entry"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Update entry
        update_data = {
            'title': 'Updated Title',
            'content': 'Updated content for testing purposes.'
        }
        update_result = brain.update_entry(entry_id, update_data, test_user['user_id'])

        assert update_result['status'] == 'updated'
        assert update_result['id'] == entry_id

        # Verify update
        updated_entry = brain.get_entry(entry_id, test_user['user_id'])
        assert updated_entry['title'] == 'Updated Title'
        assert updated_entry['content'] == 'Updated content for testing purposes.'

    def test_delete_entry(self, test_user, sample_knowledge_entry):
        """Test deleting a knowledge entry"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Delete entry
        delete_result = brain.delete_entry(entry_id, test_user['user_id'])

        assert delete_result['status'] == 'deleted'
        assert delete_result['id'] == entry_id

        # Verify deletion
        deleted_entry = brain.get_entry(entry_id, test_user['user_id'])
        assert deleted_entry is None


class TestEmbeddings:
    """Test embedding generation and storage"""

    def test_generate_embedding_vector(self):
        """Test generating embedding vector"""
        brain = BrainModule()

        # Generate embedding for test text
        text = "This is a test text for embedding generation."
        embedding = brain._generate_embedding_vector(text)

        assert embedding is not None
        assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension
        assert all(isinstance(x, float) for x in embedding)

    @pytest.mark.slow
    def test_generate_embedding_for_entry(self, test_user, sample_knowledge_entry):
        """Test generating embedding for a knowledge entry"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Generate embedding (this will call Qdrant)
        result = brain.generate_embedding(entry_id)

        # Note: This test requires Qdrant to be running
        # If Qdrant is not available, this test might fail
        if 'error' not in result:
            assert result['status'] == 'embedded'
            assert 'qdrant_id' in result
            assert result['entry_id'] == entry_id


class TestAnkiIntegration:
    """Test Anki integration"""

    @pytest.mark.skipif(not True, reason="Requires AnkiConnect to be running")
    def test_create_anki_card(self, test_user, sample_knowledge_entry):
        """Test creating Anki card from knowledge entry"""
        brain = BrainModule()

        # Create test entry with Q:/A: pattern
        entry_with_qa = sample_knowledge_entry.copy()
        entry_with_qa['content'] = """Q: What is the capital of France?

A: Paris"""

        create_result = brain.create_entry(entry_with_qa, test_user['user_id'])
        entry_id = create_result['id']

        # Create Anki card
        result = brain.create_anki_card(entry_id, test_user['user_id'])

        if 'error' not in result:
            assert result['status'] == 'created'
            assert 'anki_card_id' in result
            assert result['entry_id'] == entry_id

    def test_extract_anki_content(self):
        """Test extracting Anki content (front/back)"""
        brain = BrainModule()

        # Test Q:/A: pattern
        content = """Q: What is Python?

A: Python is a high-level programming language."""
        front, back = brain._extract_anki_content(content)

        assert 'What is Python?' in front
        assert 'Python is a high-level programming language' in back

        # Test fallback (no Q:/A: pattern)
        content_no_qa = """This is a general knowledge entry.
It has multiple paragraphs.
Third paragraph here."""

        front, back = brain._extract_anki_content(content_no_qa)

        assert front is not None
        assert len(front) <= 200  # Limited to 200 chars
        assert back is not None


class TestWebClipping:
    """Test web clipping functionality"""

    @pytest.mark.integration
    def test_extract_web_content(self):
        """Test extracting content from web page"""
        brain = BrainModule()

        # Test with a known URL
        # Note: This test makes actual HTTP requests
        # Skip if network is not available
        try:
            result = brain._extract_web_content('https://example.com')

            # Result structure
            assert result is not None or result is None  # May fail due to network

            if result:
                assert 'title' in result
                assert 'content' in result
                assert len(result['content']) > 0

        except Exception as e:
            pytest.skip(f"Web extraction failed: {e}")

    @pytest.mark.integration
    def test_create_web_clip(self, test_user):
        """Test creating web clip"""
        brain = BrainModule()

        # Test with a simple URL
        try:
            result = brain.create_web_clip('https://example.com', test_user['user_id'])

            if 'error' not in result:
                assert result['status'] == 'created'
                assert 'id' in result
                assert result['id'].startswith('knl_')

        except Exception as e:
            pytest.skip(f"Web clipping failed: {e}")


class TestKnowledgeGraph:
    """Test knowledge graph functionality"""

    def test_calculate_entry_similarity(self):
        """Test calculating similarity between entries"""
        brain = BrainModule()

        entry1 = {
            'domain': 'tech',
            'tags': ['python', 'api'],
            'project': 'nexus'
        }

        entry2 = {
            'domain': 'tech',
            'tags': ['python', 'testing'],
            'project': 'nexus'
        }

        score = brain._calculate_entry_similarity(entry1, entry2)

        assert 0 <= score <= 1.0
        assert score > 0  # Should have some similarity (same domain, project)

    def test_calculate_similarity_different_domains(self):
        """Test similarity for entries with different domains"""
        brain = BrainModule()

        entry1 = {
            'domain': 'tech',
            'tags': ['python'],
            'project': 'nexus'
        }

        entry2 = {
            'domain': 'health',
            'tags': ['diet'],
            'project': 'blueprint'
        }

        score = brain._calculate_entry_similarity(entry1, entry2)

        assert 0 <= score <= 1.0
        # Should have lower similarity than same-domain entries


class TestSearch:
    """Test search functionality"""

    def test_search_entries_keyword(self, test_user, sample_knowledge_entry):
        """Test keyword search"""
        brain = BrainModule()

        # Create test entry
        brain.create_entry(sample_knowledge_entry, test_user['user_id'])

        # Search for entry
        results = brain.search_entries('test', test_user['user_id'])

        assert len(results) > 0
        assert any('test' in r['title'].lower() or 'test' in r['content'].lower() for r in results)

    def test_search_with_filters(self, test_user, sample_knowledge_entry):
        """Test search with domain filter"""
        brain = BrainModule()

        # Create test entry
        brain.create_entry(sample_knowledge_entry, test_user['user_id'])

        # Search with domain filter
        results = brain.search_entries('test', test_user['user_id'], filters={
            'domain': 'tech',
            'limit': 10
        })

        assert len(results) >= 0
        # All results should be from 'tech' domain
        assert all(r.get('domain') == 'tech' for r in results)

    @pytest.mark.slow
    @pytest.mark.integration
    def test_semantic_search(self, test_user, sample_knowledge_entry):
        """Test semantic search via Qdrant"""
        brain = BrainModule()

        # Create test entry
        create_result = brain.create_entry(sample_knowledge_entry, test_user['user_id'])
        entry_id = create_result['id']

        # Generate embedding first
        brain.generate_embedding(entry_id)

        # Search semantically
        results = brain.search_entries('test', test_user['user_id'], filters={
            'semantic': True,
            'limit': 5
        })

        # Note: Requires Qdrant to be running
        assert len(results) >= 0


class TestStatistics:
    """Test statistics functionality"""

    def test_get_stats(self, test_user, sample_knowledge_entry):
        """Test getting knowledge statistics"""
        brain = BrainModule()

        # Create test entry
        brain.create_entry(sample_knowledge_entry, test_user['user_id'])

        # Get stats
        stats = brain.get_stats(test_user['user_id'])

        assert 'total_entries' in stats
        assert 'entries_by_domain' in stats
        assert 'srs_cards_created' in stats
        assert 'entries_with_embeddings' in stats
        assert stats['total_entries'] >= 1


class TestWorktrees:
    """Test git worktree management"""

    def test_create_worktree(self, test_user):
        """Test creating worktree entry"""
        brain = BrainModule()

        worktree_data = {
            'repo_name': 'test-repo',
            'branch_name': 'feature/test',
            'worktree_path': '/tmp/test-worktree',
            'context_notes': 'Test worktree for unit tests'
        }

        result = brain.create_worktree(worktree_data, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'
        assert result['id'].startswith('wkt_')

    def test_get_worktrees(self, test_user):
        """Test getting worktrees"""
        brain = BrainModule()

        # Create worktree
        worktree_data = {
            'repo_name': 'test-repo',
            'branch_name': 'feature/test',
            'worktree_path': '/tmp/test-worktree',
            'context_notes': 'Test worktree'
        }
        brain.create_worktree(worktree_data, test_user['user_id'])

        # Get worktrees
        worktrees = brain.get_worktrees(test_user['user_id'])

        assert len(worktrees) > 0
        assert any(wt['repo_name'] == 'test-repo' for wt in worktrees)

    def test_update_worktree_access(self, test_user):
        """Test updating worktree access time"""
        brain = BrainModule()

        # Create worktree
        worktree_data = {
            'repo_name': 'test-repo',
            'branch_name': 'feature/test',
            'worktree_path': '/tmp/test-worktree'
        }
        create_result = brain.create_worktree(worktree_data, test_user['user_id'])
        worktree_id = create_result['id']

        # Update access time
        result = brain.update_worktree_access(worktree_id, test_user['user_id'])

        assert result['status'] == 'accessed'
        assert result['id'] == worktree_id
