#!/usr/bin/env python3

import json
from collections.abc import Callable
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


PLUGINS_PATH = Path(__file__).resolve().parents[1] / "plugins.json"


def fetch_latest_version(distribution_name: str) -> str:
    request = Request(
        f"https://pypi.org/pypi/{quote(distribution_name, safe='')}/json",
        headers={"User-Agent": "Pioreactor plugin version updater"},
    )
    with urlopen(request, timeout=30) as response:
        package_data = json.load(response)

    latest_version = package_data["info"]["version"]
    if not isinstance(latest_version, str) or not latest_version:
        raise ValueError(f"PyPI returned an invalid version for {distribution_name}")
    return latest_version


def update_latest_versions(
    plugins: list[dict[str, object]],
    get_latest_version: Callable[[str], str] = fetch_latest_version,
) -> bool:
    changed = False
    for plugin in plugins:
        distribution_name = plugin.get("name")
        if not isinstance(distribution_name, str) or not distribution_name:
            raise ValueError("Every plugin must have a non-empty string name")

        latest_version = get_latest_version(distribution_name)
        if plugin.get("latest_version_available") != latest_version:
            plugin["latest_version_available"] = latest_version
            changed = True

    return changed


def main() -> None:
    plugins = json.loads(PLUGINS_PATH.read_text(encoding="utf-8"))
    if not isinstance(plugins, list):
        raise ValueError("plugins.json must contain a list")

    if update_latest_versions(plugins):
        temporary_path = PLUGINS_PATH.with_suffix(".json.tmp")
        temporary_path.write_text(
            json.dumps(plugins, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(PLUGINS_PATH)


if __name__ == "__main__":
    main()
