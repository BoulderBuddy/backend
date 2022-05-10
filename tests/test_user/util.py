from app import crud, models
from app.crud.crud_user import CRUDUser
from app.schemas.user import UserCreate, UserUpdate
from tests.utils import CRUDTestUtil

_default_user_data = UserCreate(
    first_name="Bert", surname="van Ernie", email="bert@ernie.com", is_superuser=True
).__dict__


user_crud_util = CRUDTestUtil[CRUDUser, models.User, UserCreate, UserUpdate](
    _default_user_data, crud.user
)
