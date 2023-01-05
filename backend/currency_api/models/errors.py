from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


not_found = {
    "code": 400,
    "error": {"model": HTTPError, "description": "Currency code or Date not found"},
}

date_malformed = {
    "code": 404,
    "error": {"model": HTTPError, "description": "Date malformed, expected '%d-%m-%Y'"},
}

all_errors = [not_found, date_malformed]


def get_responses(errors):  # type: ignore

    return {i["code"]: i["error"] for i in errors}
