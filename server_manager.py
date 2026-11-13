import argparse
import datetime as dt
import json
import socket
import time
from pathlib import Path


def check_server(server, timeout=2.0):
    start = time.monotonic()
    try:
        with socket.create_connection((server["host"], int(server["port"])), timeout=timeout):
            status = "online"
            error = None
    except (OSError, ValueError) as exc:
        status = "offline"
        error = str(exc)
    return {"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), "name": server["name"],
            "host": server["host"], "port": int(server["port"]), "status": status,
            "connect_ms": round((time.monotonic() - start) * 1000, 2), "error": error}


def run_checks(config, output):
    servers = json.loads(Path(config).read_text(encoding="utf-8"))["servers"]
    output.mkdir(parents=True, exist_ok=True)
    checks = [check_server(s) for s in servers]
    with (output / "history.jsonl").open("a", encoding="utf-8") as file:
        for item in checks:
            file.write(json.dumps(item) + "\n")
    summary = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
               "online": sum(x["status"] == "online" for x in checks),
               "offline": sum(x["status"] == "offline" for x in checks), "checks": checks}
    (output / "latest_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for item in checks:
        print(f'{item["name"]}: {item["status"]} ({item["connect_ms"]} ms)')
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="servers.json")
    parser.add_argument("--output", default="output")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=float, default=10)
    parser.add_argument("--count", type=int, default=0, help="0 means repeat indefinitely")
    args = parser.parse_args()
    if args.interval <= 0 or args.count < 0:
        parser.error("interval must be positive and count cannot be negative")
    i = 0
    try:
        while True:
            run_checks(args.config, Path(args.output))
            i += 1
            if args.once or (args.count and i >= args.count):
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped")


if __name__ == "__main__":
    main()
