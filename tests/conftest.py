import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app(test_config={"TESTING": True, "DATABASE": ":memory:"})
    with app.test_client() as client:
        yield client
