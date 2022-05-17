from app.api.error_http import HTTPErrorAlreadyExists, HTTPErrorNotFound

NotFoundResponse = {
    404: {"model": HTTPErrorNotFound, "description": "Resource could not be found"}
}


AlreadyExistsResponse = {
    400: {"model": HTTPErrorAlreadyExists, "description": "Resource already exists"}
}


NoContentResponse = {204: {"description": "No Content"}}
