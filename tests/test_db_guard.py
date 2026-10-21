import pytest
from sqlalchemy.engine import make_url

from config import settings
from tests.db_guard import ensure_test_database


def test_accepts_test_database_url():
    ensure_test_database("postgresql+psycopg://bloguser:blogpass@localhost/test_blog")


def test_accepts_engine_url_object():
    ensure_test_database(make_url("postgresql+psycopg://u:p@localhost/test_blog"))


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://user:pw@ep-prod.eu-central-1.aws.neon.tech/neondb",
        "postgresql+psycopg://user:pw@localhost/neondb",
        "postgresql+psycopg://user:pw@db.example.com/test_blog",
        "postgresql+psycopg://user:pw@localhost/test_blog_copy",
    ],
)
def test_rejects_non_test_database_url(url):
    with pytest.raises(pytest.exit.Exception, match="Refusing to run tests"):
        ensure_test_database(url)


def test_settings_point_at_test_database():
    ensure_test_database(settings.database_url)
