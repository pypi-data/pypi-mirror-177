import json
import os
import time
from json import JSONDecodeError
from typing import Dict, Optional

import requests
from requests import Response


def download_json(url: str, headers: Dict[str, str] = None) -> Optional[str]:
    headers = headers or {}

    max_trials: int = 3
    wait_on_retry: float = 1.0
    for trial in range(1, max_trials + 1):

        try:
            r: Response = requests.get(url, headers=headers, timeout=20)
        except requests.exceptions.ConnectionError:
            if trial == max_trials:
                raise
            else:
                time.sleep(wait_on_retry)
                continue

        if r.status_code != 200:
            if trial == max_trials:
                raise Exception(f"HTTP error: code[{r.status_code}], message: {r.reason}")
            else:
                time.sleep(wait_on_retry)
                continue
        else:
            try:
                return json.dumps(r.json())
            except JSONDecodeError:
                if trial == max_trials:
                    msg = f"Cannot decode JSON from '{url}'"
                    raise Exception(f"JSONDecodeError: {msg}")
                else:
                    time.sleep(wait_on_retry)
                    continue


def interpret_pypi(json_string):
    rj = json.loads(json_string)
    pypi_version = rj["info"]["version"]
    return pypi_version


def interpret_devpi(json_string):
    rj = json.loads(json_string)
    versions = list(rj["result"])

    def try_int(x):
        try:
            return int(x)
        except ValueError:
            return 0

    version_sorted = sorted(versions, key=lambda _: tuple(map(try_int, _.split("."))))

    v = version_sorted[-1]
    return v


def get_pip_server():
    default = "https://pypi.org/pypi"
    r = os.environ.get("PIP_INDEX_URL", default)
    if r.endswith("/"):
        r = r[:-1]
    return r


def get_last_version_fresh(package_name: str) -> Optional[str]:
    pip_server = get_pip_server()
    # logger.info(pip_server=pip_server)
    if "pypi.org" in pip_server:
        pip_server = "https://pypi.org/pypi"
        url = f"{pip_server}/{package_name}/json"
        headers = {"Accept": "application/json"}
        # noinspection PyBroadException
        try:
            j = download_json(url, headers=headers)
        except Exception:
            return None
        return interpret_pypi(j)
    else:
        headers = {"Accept": "application/json"}
        url = f"{pip_server}/{package_name}"
        # noinspection PyBroadException
        try:
            j = download_json(url, headers=headers)
        except Exception:
            return None

        return interpret_devpi(j)
