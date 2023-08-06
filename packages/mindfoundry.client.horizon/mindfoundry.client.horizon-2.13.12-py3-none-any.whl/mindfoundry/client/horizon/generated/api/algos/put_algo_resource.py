from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.algo_spec import AlgoSpec
from ...models.trading_algo import TradingAlgo
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    json_body: AlgoSpec,
) -> Dict[str, Any]:
    url = "{}/algos/{id}".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[TradingAlgo]:
    if response.status_code == 200:
        response_200 = TradingAlgo.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TradingAlgo]:
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
    json_body: AlgoSpec,
) -> Response[TradingAlgo]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: int,
    json_body: AlgoSpec,
) -> Optional[TradingAlgo]:
    """WARNING: updating an algo will not automatically re-run pipelines that use it,
    after updating an algo, you must manually re-run the pipeline to test it fully.
    """

    return sync_detailed(
        client=client,
        id=id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    json_body: AlgoSpec,
) -> Response[TradingAlgo]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: int,
    json_body: AlgoSpec,
) -> Optional[TradingAlgo]:
    """WARNING: updating an algo will not automatically re-run pipelines that use it,
    after updating an algo, you must manually re-run the pipeline to test it fully.
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            json_body=json_body,
        )
    ).parsed
