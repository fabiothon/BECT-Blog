import re

import pytest
from httpx import AsyncClient, Response

from tests.conftest import auth_header, create_test_user, login_user

LAYOUT_DIALOGS = ("createPostModal", "successModal", "errorModal")


def assert_tailwind_page(response: Response, dialogs: tuple[str, ...] = ()) -> None:
    html = response.text
    assert response.headers["content-type"].startswith("text/html")
    assert "/static/css/output.css" in html
    assert "bootstrap" not in html.lower()
    assert "data-bs-" not in html
    assert "main.css" not in html
    for dialog_id in LAYOUT_DIALOGS + dialogs:
        assert re.search(rf'<dialog[^>]*\bid="{dialog_id}"', html), dialog_id


async def create_post(client: AsyncClient) -> tuple[dict, dict]:
    user = await create_test_user(client)
    token = await login_user(client)
    response = await client.post(
        "/api/posts",
        json={"title": "Page Test Post", "content": "Line one\nLine two"},
        headers=auth_header(token),
    )
    assert response.status_code == 201
    return user, response.json()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "path",
    ["/", "/posts", "/login", "/register", "/forgot-password", "/reset-password"],
)
async def test_static_pages_render_with_tailwind(client: AsyncClient, path: str):
    response = await client.get(path)

    assert response.status_code == 200
    assert_tailwind_page(response)


@pytest.mark.anyio
async def test_account_page_has_delete_dialog(client: AsyncClient):
    response = await client.get("/account")

    assert response.status_code == 200
    assert_tailwind_page(response, ("deleteAccountModal",))


@pytest.mark.anyio
async def test_post_page_has_edit_and_delete_dialogs(client: AsyncClient):
    _, post = await create_post(client)

    response = await client.get(f"/posts/{post['id']}")

    assert response.status_code == 200
    assert_tailwind_page(response, ("editModal", "deleteModal"))
    assert "Page Test Post" in response.text


@pytest.mark.anyio
async def test_home_lists_posts(client: AsyncClient):
    _, post = await create_post(client)

    response = await client.get("/")

    assert response.status_code == 200
    assert_tailwind_page(response)
    assert f'href="http://test/posts/{post["id"]}"' in response.text


@pytest.mark.anyio
async def test_user_posts_page_renders(client: AsyncClient):
    user, _ = await create_post(client)

    response = await client.get(f"/users/{user['id']}/posts")

    assert response.status_code == 200
    assert_tailwind_page(response)
    assert f"Posts by {user['username']}" in response.text


@pytest.mark.anyio
async def test_error_page_renders_with_tailwind(client: AsyncClient):
    response = await client.get("/posts/999999")

    assert response.status_code == 404
    assert_tailwind_page(response)
    assert "404 Error" in response.text
