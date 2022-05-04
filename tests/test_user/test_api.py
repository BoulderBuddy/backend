from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud


def test_create_user_new_email(client: TestClient, db: Session) -> None:
    username = "bert@ernie.com"
    data = {"email": username}
    r = client.post("/users/", json=data)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]
