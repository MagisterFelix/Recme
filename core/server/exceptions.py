from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exception: APIException, context: dict) -> Response | None:
    response = exception_handler(exception, context)

    if response is None or response.data is None:
        return response

    payload = {
        "details": []
    }

    if response.status_code == 403:
        payload["details"].append({"detail": response.data["detail"]})
    else:
        for field, errors in response.data.items():
            if isinstance(errors, list):
                errors = " ".join(errors)

            if "unique set" in errors:
                errors = "Values must be unique."

            payload["details"].append({
                field: ". ".join(err if err[0].isupper() else err.capitalize() for err in errors.split(". "))
            })

    response.data = payload

    return response
