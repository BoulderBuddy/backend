from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schemas
from tests.conftest import TestData
from tests.utils import TestSchemas, validate_payload

from .util import exercise_crud_util

EXERCISE_ENDPOINT = "exercises"


@pytest.mark.parametrize(
    "data",
    [schemas.ExerciseCreate(name="The Dinosaur", parameters=[TestData.EXER_PARA_1])],
)
def test_create_exercise(client: TestClient, data: schemas.ExerciseCreate) -> None:
    f"""
    GIVEN request data with valid data
    WHEN endpoint /{EXERCISE_ENDPOINT}/ is called
    THEN it should return 200 and Exercise in valid json schema
    """
    r = client.post(f"/{EXERCISE_ENDPOINT}/", data=data.json())

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE)


@pytest.mark.parametrize(
    "data",
    [{"parameters": [TestData.EXER_PARA_1.json()]}, {"name": "The Dinosaur"}, {}],
)
def test_create_exercise_invalid(client: TestClient, data: Dict[str, Any]) -> None:
    f"""
    GIVEN request data with missing or invalid data
    WHEN endpoint /{EXERCISE_ENDPOINT}/ is called
    THEN it should return status 422
    """
    r = client.post(f"/{EXERCISE_ENDPOINT}/", json=data)

    assert r.status_code == 422
    assert r.json() is not None


def test_read_all_exercise(client: TestClient, db: Session) -> None:
    f"""
    GIVEN Exercises stored in the database
    WHEN endpoint /{EXERCISE_ENDPOINT}/ is called
    THEN it should return list of Exercises in valid json schema
    """
    exercise_crud_util.insert_into_db(db)

    r = client.get(f"/{EXERCISE_ENDPOINT}/")

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE_LIST)


@pytest.mark.parametrize(
    "data",
    [{"parameters": [TestData.EXER_PARA_1.__dict__]}, {"name": "The Dinosaur"}, {}],
)
def test_update_exercise(client: TestClient, db: Session, data: Dict[str, Any]) -> None:
    f"""
    GIVEN ID of Exercise stored in database
    WHEN endpoint /{EXERCISE_ENDPOINT}/<exercise-id>/ is called
    THEN it should return Exercise in valid json schema
    """
    id = exercise_crud_util.insert_into_db(db).id

    r = client.put(f"/{EXERCISE_ENDPOINT}/{id}", json=data)

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE)


def test_update_exercise_not_found(client: TestClient) -> None:
    f"""
    GIVEN ID of Exercise missing in the database
    WHEN endpoint /{EXERCISE_ENDPOINT}/<exercise-id>/ is called
    THEN it should return status 404
    """
    id = 42

    r = client.put(f"/{EXERCISE_ENDPOINT}/{id}", json={})

    assert r.status_code == 404
    assert r.json() is not None
