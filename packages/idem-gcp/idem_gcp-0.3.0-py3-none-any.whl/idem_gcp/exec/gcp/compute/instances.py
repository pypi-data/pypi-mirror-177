async def list_(hub, ctx):
    """Return a list of items"""
    return {
        "comment": "sample list",
        "ret": [],
        "status": True,
    }


async def get(hub, ctx, name: str):
    """Return a single named item"""
    return {
        "comment": "sample get",
        "ret": name,
        "status": True,
    }
