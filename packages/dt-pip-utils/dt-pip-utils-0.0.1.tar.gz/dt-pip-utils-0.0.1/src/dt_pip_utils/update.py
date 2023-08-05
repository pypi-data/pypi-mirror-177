import os
from typing import Optional

import requirements
from requirements.requirement import Requirement

from .versions import get_last_version_fresh

__all__ = ["update_versions"]


def update_versions(fin: str, fout: Optional[str] = None):
    fout = fout or fin + ".resolved"

    if not os.path.exists(fin):
        print(f"Requirement file '{fin}' does not exist")
        return

    print(f"Now updating requirements files '{fin}' -> '{fout}'")

    resolved = []
    with open(fin) as fd:
        req: Requirement
        for req in requirements.parse(fd):
            todo = (len(req.specs) == 0) or \
                   (len(req.specs) == 1 and req.specs[0][0] in (">=", ">"))
            if todo:
                v = get_last_version_fresh(req.name)
                if v is None:
                    msg = f"Cannot find the package '{req.name}'"
                    raise Exception(msg)

                print(f"Updated package: {req.name} to {v}")
                req.specs = [("==", v)]
            else:
                print(f"Skipping spec {req}: {req.specs}")

            ss = ",".join(f"{a}{b}" for a, b in req.specs)
            s2 = f"{req.name}{ss}"
            resolved.append(s2)

    # compile output file
    res = "\n".join(resolved)
    # write file to disk
    with open(fout, "wt") as buf:
        buf.write(res)
