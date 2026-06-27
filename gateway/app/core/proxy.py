import httpx

from fastapi import Request, HTTPException

from app.core.service import SERVICES


async def proxy_request(
        service: str,
        path: str,
        request: Request
):

    base_url = SERVICES.get(service)

    if not base_url:
        raise HTTPException(
            status_code=404,
            detail="Service Not Found"
        )

    url = f"{base_url}/{path}"

    async with httpx.AsyncClient() as client:

        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body(),
        )

    return response.json()