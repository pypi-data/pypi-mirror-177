from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.cockroach_cloud_set_egress_traffic_policy_response_200 import (
    CockroachCloudSetEgressTrafficPolicyResponse200,
)
from ...models.cockroach_cloud_set_egress_traffic_policy_set_egress_traffic_policy_request import (
    CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
)
from ...types import Response


def _get_kwargs(
    cluster_id: str,
    *,
    client: Client,
    json_body: CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
) -> Dict[str, Any]:
    url = "{}/api/v1/clusters/{cluster_id}/networking/egress-rules/egress-traffic-policy".format(
        client.base_url, cluster_id=cluster_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    if response.status_code == 200:
        response_200 = CockroachCloudSetEgressTrafficPolicyResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, response.json())
        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, response.json())
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, response.json())
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, response.json())
        return response_404
    if response.status_code == 500:
        response_500 = cast(Any, response.json())
        return response_500
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    cluster_id: str,
    *,
    client: Client,
    json_body: CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
) -> Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    """Outbound traffic management

    Args:
        cluster_id (str):
        json_body (CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest):
            SetEgressTrafficPolicyRequest is the input for the SetEgressTrafficPolicy RPC.

    Returns:
        Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    cluster_id: str,
    *,
    client: Client,
    json_body: CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
) -> Optional[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    """Outbound traffic management

    Args:
        cluster_id (str):
        json_body (CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest):
            SetEgressTrafficPolicyRequest is the input for the SetEgressTrafficPolicy RPC.

    Returns:
        Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]
    """

    return sync_detailed(
        cluster_id=cluster_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    cluster_id: str,
    *,
    client: Client,
    json_body: CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
) -> Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    """Outbound traffic management

    Args:
        cluster_id (str):
        json_body (CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest):
            SetEgressTrafficPolicyRequest is the input for the SetEgressTrafficPolicy RPC.

    Returns:
        Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    cluster_id: str,
    *,
    client: Client,
    json_body: CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest,
) -> Optional[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]:
    """Outbound traffic management

    Args:
        cluster_id (str):
        json_body (CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest):
            SetEgressTrafficPolicyRequest is the input for the SetEgressTrafficPolicy RPC.

    Returns:
        Response[Union[Any, CockroachCloudSetEgressTrafficPolicyResponse200]]
    """

    return (
        await asyncio_detailed(
            cluster_id=cluster_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
