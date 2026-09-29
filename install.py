"""pqm-g5-test's install step: what a companion program's setup looks like to PQM.

    python install.py <part>

PQM's pod agent runs this as an extension's install step (PQM session G.5), in
the checkout it made at a pinned commit. It does real, checkable work with the
standard library only: it reads this checkout's own files, hashes them, and
writes ``installed-<part>.json`` into the extension's folder on the pod
(``PQM_EXT_DIR``), where the extension's job reads it back. Exit 0 means
installed; anything else is a failed install, and PQM stops the boot by name.

``fail`` is the part that fails on purpose: it prints why and exits 3.
"""

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(argv):
    part = argv[1] if len(argv) > 1 else "all"
    if part == "fail":
        print("pqm-g5-test: this install step fails on purpose (part 'fail')")
        return 3
    started = time.time()
    digest = hashlib.sha256()
    names = sorted(p.name for p in HERE.iterdir() if p.is_file())
    for name in names:
        digest.update(name.encode())
        digest.update((HERE / name).read_bytes())
    folder = Path(os.environ.get("PQM_EXT_DIR") or HERE)
    marker = {
        "part": part,
        "files": names,
        "sha256": digest.hexdigest(),
        "python": platform.python_version(),
        "repo": str(HERE),
        "seconds": round(time.time() - started, 3),
    }
    out = folder / ("installed-%s.json" % part)
    out.write_text(json.dumps(marker, indent=1, sort_keys=True), encoding="utf-8")
    print("pqm-g5-test: installed part %r, %d files, sha256 %s" % (part, len(names),
                                                                    marker["sha256"][:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
