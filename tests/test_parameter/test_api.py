from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.conftest import TestData
from tests.utils import TestSchemas, validate_payload

from .util import exercise_parameter_crud_util

PARAMETER_ENDPOINT_V1 = "/parameters"


@pytest.mark.parametrize(
    "data",
    [{"name": "reps", "unit_type": "int"}],
)
def test_create_exercise_parameter(client: TestClient, data: Dict[str, Any]) -> None:
    f"""
    GIVEN request data with valid data
    WHEN endpoint {PARAMETER_ENDPOINT_V1}/ is called
    THEN it should return 200 and ExerciseParameter in valid json schema
    """
    r = client.post(f"{PARAMETER_ENDPOINT_V1}/", json=data)

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE_PARAMETER)


@pytest.mark.parametrize(
    "data",
    [{"name": "reps"}, {"unit_type": "int"}, {}],
)
def test_create_exercise_parameter_invalid(
    client: TestClient, data: Dict[str, Any]
) -> None:
    f"""
    GIVEN request data with missing or invalid data
    WHEN endpoint {PARAMETER_ENDPOINT_V1}/ is called
    THEN it should return status 422
    """
    r = client.post(f"{PARAMETER_ENDPOINT_V1}/", json=data)

    assert r.status_code == 422
    assert r.json() is not None


def test_read_all_exercise_parameter(client: TestClient, db: Session) -> None:
    f"""
    GIVEN ExerciseParameters stored in the database
    WHEN endpoint {PARAMETER_ENDPOINT_V1}/ is called
    THEN it should return list of ExerciseParameters in valid json schema
    """
    exercise_parameter_crud_util.insert_into_db(db)

    r = client.get(f"{PARAMETER_ENDPOINT_V1}/")

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE_PARAMETER_LIST)


@pytest.mark.parametrize(
    "data",
    [{"name": "reps"}, {"unit_type": "int"}, {}],
)
def test_update_exercise_parameter(client: TestClient, data: Dict[str, Any]) -> None:
    f"""
    GIVEN ID of ExerciseParameter stored in database
    WHEN endpoint {PARAMETER_ENDPOINT_V1}/<parameter-id>/ is called
    THEN it should return ExerciseParameter in valid json schema
    """
    id = TestData.EXER_PARA_1.id

    r = client.put(f"{PARAMETER_ENDPOINT_V1}/{id}", json=data)

    assert r.status_code == 200
    validate_payload(r.json(), TestSchemas.EXERCISE_PARAMETER)


def test_update_exercise_parameter_not_found(client: TestClient) -> None:
    f"""
    GIVEN ID of ExerciseParameter missing in the database
    WHEN endpoint {PARAMETER_ENDPOINT_V1}/<parameter-id>/ is called
    THEN it should return status 404
    """
    id = 42

    r = client.put(f"{PARAMETER_ENDPOINT_V1}/{id}", json={})

    assert r.status_code == 404
    assert r.json() is not None
