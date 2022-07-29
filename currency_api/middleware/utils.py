from fastapi import Request


def request_url(request: Request) -> str:
    query = request.url.components.query
    path = request.url.components.path

    if query:
        return f"{path}&{query}"

    return path
