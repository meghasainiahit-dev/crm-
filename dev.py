import subprocess

services = [
    ("company", 8001),
    ("department", 8002),
]

processes = []

for path, port in services:
    p = subprocess.Popen(
        [
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
        ],
        cwd=path,
    )
    processes.append(p)

for p in processes:
    p.wait()