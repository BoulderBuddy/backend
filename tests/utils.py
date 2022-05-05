import json
import pathlib

from jsonschema import RefResolver, validate


class TestSchemas:
    USER: str = "User.json"
    USER_LIST: str = "UserList.json"


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/schemas")
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema,  # it's used to resolve the file inside schemas correctly
        ),
    )
