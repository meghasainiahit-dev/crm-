import json
import subprocess
import time
from pathlib import Path

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

URLS_FILE = ROOT / "urlsbase.json"

SERVICES_DIR = ROOT / "services"

GATEWAY_DIR = ROOT / "gateway"

processes = []


# -------------------------------------------------------
# Load Services
# -------------------------------------------------------

def load_services():

    if not URLS_FILE.exists():
        raise FileNotFoundError(
            f"urlsbase.json not found : {URLS_FILE}"
        )

    with open(URLS_FILE, "r") as f:
        data = json.load(f)

    return data["services"]


# -------------------------------------------------------
# Start Gateway
# -------------------------------------------------------

def start_gateway():

    if not GATEWAY_DIR.exists():
        print("⚠ Gateway folder not found")
        return

    print("🚀 Starting Gateway : 8000")

    process = subprocess.Popen(
        [
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        cwd=GATEWAY_DIR,
    )

    processes.append(process)


# -------------------------------------------------------
# Start Services
# -------------------------------------------------------

def start_services():

    services = load_services()

    for service in services:

        if not service.get("enabled", True):
            continue

        name = service["name"]
        port = service["port"]

        service_path = SERVICES_DIR / name

        if not service_path.exists():
            print(f"❌ Service folder not found : {service_path}")
            continue

        print(f"🚀 Starting {name} : {port}")

        process = subprocess.Popen(
            [
                "uvicorn",
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                str(port),
            ],
            cwd=service_path,
        )

        processes.append(process)

        time.sleep(0.5)


# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("Starting Development Environment")
    print("=" * 60)

    start_gateway()

    start_services()

    print("\n")

    print("=" * 60)
    print("Running Services")
    print("=" * 60)

    print("Gateway".ljust(15), "http://localhost:8000")

    for service in load_services():

        if service.get("enabled", True):

            print(
                service["name"].title().ljust(15),
                f"http://localhost:{service['port']}/docs"
            )

    print("=" * 60)

    for process in processes:
        process.wait()