#!/usr/bin/env python3
import argparse
import http.server
import socketserver
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Serve geoflow-template preview files.")
    parser.add_argument("--port", type=int, default=45731)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Skill root directory"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    handler = lambda *h_args, **h_kwargs: http.server.SimpleHTTPRequestHandler(
        *h_args, directory=str(root), **h_kwargs
    )
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"Serving skill root: {root}")
        print(f"Preview URL: http://127.0.0.1:{args.port}/preview/qiaomu-editorial-20260418/index.html")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
