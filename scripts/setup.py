from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

VENV = ROOT / "env"

SERVICES = ROOT / "services"

GATEWAY = ROOT / "gateway"


def run(cmd, cwd=None):

    print(" ".join(cmd))

    subprocess.check_call(cmd, cwd=cwd)




if not VENV.exists():

    print("Creating Virtual Environment...")

    run([
        sys.executable,
        "-m",
        "venv",
        "env"
    ], cwd=ROOT)



if sys.platform == "win32":

    python = ROOT / "env" / "Scripts" / "python.exe"

else:

    python = ROOT / "env" / "bin" / "python"



run([
    str(python),
    "-m",
    "pip",
    "install",
    "--upgrade",
    "pip"
])



root_req = ROOT / "requirements.txt"

if root_req.exists():

    run([
        str(python),
        "-m",
        "pip",
        "install",
        "-r",
        str(root_req)
    ])



gateway_req = GATEWAY / "requirements.txt"

if gateway_req.exists():

    run([
        str(python),
        "-m",
        "pip",
        "install",
        "-r",
        str(gateway_req)
    ])


for service in SERVICES.iterdir():

    if not service.is_dir():
        continue

    req = service / "requirements.txt"

    if req.exists():

        print(f"\nInstalling : {service.name}")

        run([
            str(python),
            "-m",
            "pip",
            "install",
            "-r",
            str(req)
        ])

print("\nSetup Completed Successfully.")