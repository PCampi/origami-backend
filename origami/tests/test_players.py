"""Test for the players resource."""

from falcon import testing
import pytest

from ..main_app import create_app


@pytest.fixture()
def client():
    """Create a client context for testing."""
    return testing.TestClient(create_app(db_mode_memory=True))


def test_get_player(client):
    """Test for the /players endpoint."""
    result = client.simulate_get("/players/1")
    truth = {
        "id": 1,
        "name": "Giovannino",
        "age": 9,
        "gender": "male"
    }

    assert result.json == truth
