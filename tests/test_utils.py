import pytest
from pygit.utils import hash_content

def test_hash_content():
    """Test the hashing function."""
    content = "Hello, PyGit!"
    hashed = hash_content(content)
    assert len(hashed) == 40
    assert isinstance(hashed, str)
