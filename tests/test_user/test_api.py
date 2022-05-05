from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from tests.utils import TestSchemas, validate_payload

USER_ENDPOINT = "users"


@pytest.mark.parametrize(
    "data",
    [
        {
            "email": "bert@ernie.com",
            "first_name": "bert",
            "surname": "van ernie",
            "is_superuser": False,
        }
    ],
)
def test_create_user_new_email(client: TestClient, data: Dict[str, Any]) -> None:
    f"""
    GIVEN request data with valid data
    WHEN endpoint /{USER_ENDPOINT}/ is called
    THEN it should return 200 and User in valid json schema
    """
    r = client.post(f"/{USER_ENDPOINT}/", json=data)
    created_user = r.json()

    assert 200 == r.status_code
    assert data["email"] == created_user["email"]
    validate_payload(created_user, TestSchemas.USER)


@pytest.mark.parametrize(
    "data",
    [
        {"email": 123},
        {"email": "geen email adres hehehehe"},
        {"surname": "John Doe"},
        {"email": None},
        {
            "email": "bert@ernie.com",
            "first_name": "bert",
            "surname": "van ernie",
            "is_superuser": 123,
        },
        {},
    ],
)
def test_create_user_unprocessable_entity(
    client: TestClient, data: Dict[str, Any]
) -> None:
    f"""
    GIVEN request data with missing or invalid data
    WHEN endpoint /{USER_ENDPOINT}/ is called
    THEN it should return status 422
    """
    r = client.post(f"/{USER_ENDPOINT}/", json=data)

    assert r.status_code == 422
    assert r.json() is not None


def test_read_all_users(client: TestClient, db: Session) -> None:
    f"""
    GIVEN Users stored in the database
    WHEN endpoint /{USER_ENDPOINT}/ is called
    TTHEN it should return list of User in valid json schema
    """
    user = UserCreate(email="bert@ernie.com")
    crud.user.create(db, obj_in=user)

    r = client.get(f"/{USER_ENDPOINT}/")

    validate_payload(r.json(), TestSchemas.USER_LIST)


def test_read_user(client: TestClient, db: Session) -> None:
    f"""
    GIVEN ID of User stored in the database
    WHEN endpoint /{USER_ENDPOINT}/<user-id>/ is called
    THEN it should return User in valid json schema
    """
    user = UserCreate(email="bert@ernie.com")
    user_db = crud.user.create(db, obj_in=user)
    id = user_db.id

    r = client.get(f"/{USER_ENDPOINT}/{id}")

    validate_payload(r.json(), TestSchemas.USER)


def test_read_user_not_found(client: TestClient) -> None:
    f"""
    GIVEN ID of User missing in the database
    WHEN endpoint /{USER_ENDPOINT}/<user-id>/ is called
    THEN it should return status 404
    """
    id = 42

    r = client.get(f"/{USER_ENDPOINT}/{id}")

    assert r.status_code == 404
    assert r.json() is not None
