"""pqm-g5-test's service: a process that stays up beside Forge on the pod.

    python serve.py <port>

PQM's pod agent starts this as an extension's service (PQM session G.5) and
waits for ``GET /health`` to answer before the boot counts as done. It listens
on 127.0.0.1 only: nothing outside the pod reaches it, and an extension's job
talks to it on the pod. Standard library only.

    GET /health  -> {"ok": true, "service": "pqm-g5-test", "pid": ..., "up_s": ...}
    GET /echo?x= -> {"echo": "..."}
"""

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

STARTED = time.time()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - http.server's name
        url = urlsplit(self.path)
        if url.path == "/health":
            body = {"ok": True, "service": "pqm-g5-test", "pid": os.getpid(),
                    "up_s": round(time.time() - STARTED, 1)}
        elif url.path == "/echo":
            body = {"echo": (parse_qs(url.query).get("x") or [""])[0]}
        else:
            self.send_error(404)
            return
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        sys.stdout.write("pqm-g5-test: " + (fmt % args) + "\n")
        sys.stdout.flush()


def main(argv):
    port = int(argv[1]) if len(argv) > 1 else 8210
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("pqm-g5-test: serving on 127.0.0.1:%d" % port, flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main(sys.argv)
