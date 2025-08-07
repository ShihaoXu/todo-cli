import pytest
from planner import db

class TestDB:
    def test_no_path_fail(self):
        with pytest.raises(TypeError):
            db.DB()