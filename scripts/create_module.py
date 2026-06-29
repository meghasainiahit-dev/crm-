from pathlib import Path
import sys
import json

# ==========================================================
# Templates
# ==========================================================

TEMPLATE = {
    "app/database/database.py": """# Database Connection

def connect_db():
    pass
""",

    "app/model/model.py": """# Models
""",

    "app/routes/routes.py": """from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"message": "Service Running"}
""",

    "app/schema/schema.py": """# Pydantic Schemas
""",

    "app/service/service.py": """# Business Logic
""",

    "app/main.py": """from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="SERVICE_NAME")

app.include_router(router)
""",

    ".env": """PORT=8000

DATABASE_URL=

REDIS_URL=

JWT_SECRET=
""",

    "requirements.txt": """fastapi
uvicorn
python-dotenv
httpx
""",

    "README.md": """# SERVICE_NAME Service
"""
}

# ==========================================================
# Update urlsbase.json
# ==========================================================


def update_urlsbase(service_name: str):

    json_file = Path("urlsbase.json")

    data = {
        "services": []
    }

    if json_file.exists():

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        except HTTPException:
            data = {"services": []}

    # Duplicate Check
    for service in data["services"]:

        if service["name"] == service_name:
            print("⚠ Service already exists inside urlsbase.json")
            return

    # Auto Port
    port = 8001 + len(data["services"])

    data["services"].append(
        {
            "name": service_name,
            "port": port,
            "host": f"http://localhost:{port}",
            "base_url": f"/api/v1/{service_name}",
            "enabled": True
        }
    )

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("✅ urlsbase.json updated")


# ==========================================================
# Create Service
# ==========================================================

def create_service(service_name: str):

    services_root = Path("services")

    services_root.mkdir(exist_ok=True)

    root = services_root / service_name

    for file_path, content in TEMPLATE.items():

        full_path = root / file_path

        full_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not full_path.exists():

            full_path.write_text(
                content.replace(
                    "SERVICE_NAME",
                    service_name.title()
                ),
                encoding="utf-8"
            )

    packages = [
        "app",
        "app/database",
        "app/model",
        "app/routes",
        "app/schema",
        "app/service",
    ]

    for package in packages:

        init_file = root / package / "__init__.py"

        init_file.touch(exist_ok=True)

    update_urlsbase(service_name)

    print(f"\n✅ Service '{service_name}' created successfully.")
    print(f"📂 Location : {root.absolute()}")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("\nUsage:")
        print("python create_module.py company\n")

        sys.exit()

    create_service(sys.argv[1])