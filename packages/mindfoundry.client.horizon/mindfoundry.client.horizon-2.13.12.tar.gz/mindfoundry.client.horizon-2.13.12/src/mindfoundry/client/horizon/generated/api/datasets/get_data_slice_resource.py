from io import BytesIO
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...types import UNSET, File, Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    start: int,
    stop: int,
) -> Dict[str, Any]:
    url = "{}/datasets/{id}/data_slice".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "start": start,
        "stop": stop,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[File]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: int,
    start: int,
    stop: int,
) -> Response[File]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        start=start,
        stop=stop,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: int,
    start: int,
    stop: int,
) -> Optional[File]:
    """  """

    return sync_detailed(
        client=client,
        id=id,
        start=start,
        stop=stop,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    start: int,
    stop: int,
) -> Response[File]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        start=start,
        stop=stop,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: int,
    start: int,
    stop: int,
) -> Optional[File]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            start=start,
            stop=stop,
        )
    ).parsed
