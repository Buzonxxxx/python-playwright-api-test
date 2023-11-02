import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def user_ids():
    ids = []
    yield ids


@pytest.fixture(scope="session")
def user_api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://reqres.in"
    )
    yield request_context
    request_context.dispose()


def test_create_user(user_api_request_context: APIRequestContext, user_ids) -> None:
    payload = {
        "name": "Ramadheer Singh",
        "job": "Rangdari"
    }

    response = user_api_request_context.post(url=f"/api/users", data=payload)
    assert response.ok

    json_response = response.json()
    print("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == payload.get("name")
    user_ids.append(json_response["id"])


def test_get_user_not_found(user_api_request_context: APIRequestContext, user_ids) -> None:
    response = user_api_request_context.get(url=f"/api/users/{user_ids[0]}")
    assert response.status == 404

    json_response = response.json()
    print("Get User API Response - User Not Found:\n{}".format(json_response))


def test_get_user_happy_flow(user_api_request_context: APIRequestContext) -> None:
    response = user_api_request_context.get(url=f"/api/users/2")
    assert response.status == 200

    json_response = response.json()
    print("Get User API Response - Happy Flow:\n{}".format(json_response))
    assert json_response["data"]["id"] == 2
