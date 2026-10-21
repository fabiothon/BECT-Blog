import pytest
from sqlalchemy.engine import URL, make_url

TEST_DB_HOST = "localhost"
TEST_DB_NAME = "test_blog"


def ensure_test_database(url: str | URL) -> None:
    parsed = make_url(url)
    if parsed.host != TEST_DB_HOST or parsed.database != TEST_DB_NAME:
        pytest.exit(
            f"Refusing to run tests against {parsed.host}/{parsed.database}, "
            f"expected {TEST_DB_HOST}/{TEST_DB_NAME}",
            returncode=1,
        )
