from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.on_demand_predict_form import OnDemandPredictForm
from ...models.predict_response_list import PredictResponseList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    json_body: OnDemandPredictForm,
) -> Dict[str, Any]:
    url = "{}/pipelines/{id}/on-demand/predict".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[PredictResponseList]:
    if response.status_code == 200:
        response_200 = PredictResponseList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PredictResponseList]:
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
    json_body: OnDemandPredictForm,
) -> Response[PredictResponseList]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: int,
    json_body: OnDemandPredictForm,
) -> Optional[PredictResponseList]:
    """  """

    return sync_detailed(
        client=client,
        id=id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    json_body: OnDemandPredictForm,
) -> Response[PredictResponseList]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: int,
    json_body: OnDemandPredictForm,
) -> Optional[PredictResponseList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            json_body=json_body,
        )
    ).parsed
