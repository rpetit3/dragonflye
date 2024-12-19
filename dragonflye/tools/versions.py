

def get_versions(tools: list) -> dict:
    """
    Get the versions of the tools in the list.

    Args:
        tools (list): List of tools to get the versions of.

    Returns:
        dict: Dictionary of tool versions.
    """
    versions = {}
    for tool in tools:
        versions[tool] = subprocess.check_output([tool, "--version"]).decode("utf-8").strip()
    return versions
