async def handle_operation(hub, ctx, operation_id: str, resource_type: str):
    operation_result = {
        "comment": [],
        "result": True,
        "rerun_data": None,
        "resource_id": None,
    }

    if "/zones/" in operation_id:
        get_ret = await hub.exec.gcp_api.client.compute.zone_operations.get(
            ctx, resource_id=operation_id
        )
        operation_type = "compute.zone_operations"
    elif "/regions/" in operation_id:
        get_ret = await hub.exec.gcp_api.client.compute.region_operations.get(
            ctx, resource_id=operation_id
        )
        operation_type = "compute.region_operations"
    elif "/global/" in operation_id:
        get_ret = await hub.exec.gcp_api.client.compute.global_operations.get(
            ctx, resource_id=operation_id
        )
        operation_type = "compute.global_operations"
    else:
        operation_result["result"] = False
        operation_result["comment"].append(
            f"Cannot determine operation scope (zonal/regional/global) {operation_id}"
        )
        return operation_result

    if not get_ret["result"] or not get_ret["ret"]:
        operation_result["result"] = False
        operation_result["comment"] = get_ret["comment"]
        return operation_result

    if get_ret["ret"]["status"] != "DONE":
        operation_result["result"] = False
        operation_result[
            "rerun_data"
        ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            get_ret["ret"].get("selfLink"), operation_type
        )
        operation_result["comment"] += get_ret["comment"]
        return operation_result

    if get_ret["ret"].get("error"):
        operation_result["result"] = False
        operation_result["comment"] += str(get_ret["ret"].get("error", {}))
        return operation_result

    operation_result[
        "resource_id"
    ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        get_ret["ret"].get("targetLink"), resource_type
    )

    return operation_result
