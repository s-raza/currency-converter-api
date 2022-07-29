from fastapi import Request


def request_url(request: Request) -> str:
    """
    Utility function to get combination of API path and query

    :param request: :obj:`fastapi.Request` object.
    :type request: required

    :return: :obj:`str`
    """
    query = request.url.components.query
    path = request.url.components.path

    if query:
        return f"{path}&{query}"

    return path
