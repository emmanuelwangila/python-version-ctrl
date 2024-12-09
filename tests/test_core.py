
import os
import pytest
from pygit.core import initialize_repo, stage_file, commit

REPO_DIR = ".pygit"

@pytest.fixture
def setup_repo():
    """Fixture to initialize a repository and clean up after tests."""
    initialize_repo()
    yield
    if os.path.exists(REPO_DIR):
        for root, dirs, files in os.walk(REPO_DIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(REPO_DIR)

def test_initialize_repo(setup_repo):
    """Test repository initialization."""
    assert os.path.exists(REPO_DIR)
    assert os.path.exists(os.path.join(REPO_DIR, "objects"))
    assert os.path.exists(os.path.join(REPO_DIR, "branches"))

def test_stage_file(setup_repo, tmp_path):
    """Test staging a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test.")
    stage_file(str(test_file))
    index_path = os.path.join(REPO_DIR, "index")
    assert os.path.exists(index_path)

def test_commit(setup_repo, tmp_path):
    """Test committing staged changes."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test.")
    stage_file(str(test_file))
    commit("Initial commit")
    objects_dir = os.path.join(REPO_DIR, "objects")
    assert len(os.listdir(objects_dir)) > 0
