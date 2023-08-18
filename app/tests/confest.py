import pytest

from app.database.connection import get_session
import pytest

from app.database.connection import get_session


@pytest.fixture(scope="session")
def test_session():
    return get_session()