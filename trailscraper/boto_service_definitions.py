"""Helper Methods to get service definition information out of the boto library"""

from __future__ import annotations

import fnmatch
import gzip
import json
from importlib import resources

# from importlib.abc import Traversable
from botocore.loaders import Loader


def boto_service_definition_files() -> list[str]:
    """Return paths to all service definition files from botocore"""

    botocore_data_dir = resources.files("botocore") / "data"
    stack = [botocore_data_dir]
    files = []
    while stack:
        p = stack.pop()
        for item in p.iterdir():
            if item.is_dir():
                stack.append(item)
            elif fnmatch.fnmatch(item.name, "service-*.json.gz"):
                files.append(str(item))
    return files


def service_definition_file(servicename):
    """Returns the path to the most recent service definition file for a service"""

    service_definitions_for_service = fnmatch.filter(
        boto_service_definition_files(),
        f"**/{servicename}/*/service-*.json.gz",
    )

    service_definitions_for_service.sort()

    return service_definitions_for_service[-1]


def operation_definition(servicename: str, operationname: str):
    """Returns the operation definition for a specific service and operation"""
    file = service_definition_file(servicename)
    _, path = file.split("/botocore/")
    r = resources.files("botocore") / path
    service_definition = json.loads(gzip.decompress(r.read_bytes()))
    return service_definition["operations"][operationname]


def main():
    # print(resources.files("botocore") / "data")
    print(operation_definition("ec2", "ImportImage"))


if __name__ == "__main__":
    main()
