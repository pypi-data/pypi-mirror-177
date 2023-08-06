""" """

__contracts__ = ["resource"]

from dataclasses import field
from dataclasses import make_dataclass
from typing import Any, Dict


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    auto_create_subnetworks: bool = False,
    description: str = None,
    enable_ula_internal_ipv6: bool = False,
    internal_ipv6_range: str = None,
    i_pv4_range: str = None,
    mtu: int = 1500,
    network_firewall_policy_enforcement_order: str = None,
    routing_config: make_dataclass(
        "NetworkRoutingConfig",
        [
            ("routing_mode", str, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    r"""Creates a network in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str):
            Project ID for this request.

        routing_config({}, Optional):
            The network-level routing configuration for this network. Used by Cloud Router to determine what type of network-wide routing behavior to enforce. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.

        auto_create_subnetworks(bool, Optional):
            Must be set to create a VPC network. If not set, a legacy network is created. When set to true, the VPC network is created in auto mode. When set to false, the VPC network is created in custom mode. An auto mode VPC network starts with one subnet per region. Each subnet has a predetermined range as described in Auto mode VPC network IP ranges. For custom mode VPC networks, you can add subnets using the subnetworks insert method. Defaults to None.

        internal_ipv6_range(str, Optional):
            When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. . Defaults to None.

        network_firewall_policy_enforcement_order(str, Optional):
            The network firewall policy enforcement order. Can be either AFTER_CLASSIC_FIREWALL or BEFORE_CLASSIC_FIREWALL. Defaults to AFTER_CLASSIC_FIREWALL if the field is not specified. Defaults to None.

        enable_ula_internal_ipv6(bool, Optional):
            Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. . Defaults to None.

        i_pv4_range(str, Optional):
            Deprecated in favor of subnet mode networks. The range of internal addresses that are legal on this network. This range is a CIDR specification, for example: 192.168.0.0/16. Provided by the client when the network is created. Defaults to None.

        mtu(int, Optional):
            Maximum Transmission Unit in bytes. The minimum value for this field is 1300 and the maximum value is 8896. The suggested value is 1500, which is the default MTU used on the Internet, or 8896 if you want to use Jumbo frames. If unspecified, the value defaults to 1460. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    result["comment"].append(
        "No-op: There is no create/update function for gcp.compute.networks"
    )

    return result


async def absent(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified network.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-network:
              gcp.compute.networks.absent:
                - resource_id: projects/tango-gcp/global/networks/my-network

    """
    result = {
        "comment": [],
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "result": True,
    }

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if ctx.test:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.compute.networks", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        # First iteration; invoke instance's delete()
        delete_ret = await hub.exec.gcp_api.client.compute.networks.delete(
            ctx, resource_id=resource_id
        )
        if delete_ret["ret"]:
            if "compute#operation" in delete_ret["ret"].get("kind"):
                result["result"] = False
                result["comment"] += delete_ret["comment"]
                result[
                    "rerun_data"
                ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                    delete_ret["ret"].get("selfLink"), "compute.global_operations"
                )
                return result

    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.networks"
        )
        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    if not resource_id:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                "gcp.compute.networks", name
            )
        )

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment("gcp.compute.networks", name)
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Retrieves the list of networks available to the specified project.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:

        .. code-block:: bash

            $ idem describe gcp.compute.networks

    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp_api.client.compute.networks.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.networks {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]["items"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.networks.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
