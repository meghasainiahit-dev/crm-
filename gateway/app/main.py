from fastapi import FastAPI
from fastapi import Request

from app.core.proxy import proxy_request

app = FastAPI()


@app.api_route(
    "/api/v1/{service}/{path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
async def gateway(
        service: str,
        path: str,
        request: Request
):

    return await proxy_request(
        service,
        path,
        request
    )